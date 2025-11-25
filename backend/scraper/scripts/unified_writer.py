# -*- coding: utf-8 -*-
import os
import json
import time
from pathlib import Path
from collections import deque

import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]  # ajuste si besoin
OUTPUT_FILE = BASE_DIR / "data" / "offres_unifiees.csv"
INDEX_FILE = BASE_DIR / "data" / "offres_unifiees.index.json"
LOCK_FILE = BASE_DIR / "data" / "offres_unifiees.lock"

UNIFIED_COLUMNS = [
    "job_id",
    "source",
    "title",
    "company",
    "region",
    "sector",
    "short_description",
    "full_description",
    "education",
    "experience",
    "contract",
    "skills",
    "salary",
    "date",
    "url"
]

MAX_JOBS = 500  # configurable


# ---- simple cross-process lock using atomic file creation ----
def acquire_lock(timeout=30):
    start = time.time()
    while True:
        try:
            fd = os.open(str(LOCK_FILE), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, str(os.getpid()).encode())
            os.close(fd)
            return
        except FileExistsError:
            if time.time() - start > timeout:
                raise TimeoutError("Impossible d'acquérir le lock (timeout).")
            time.sleep(0.05)


def release_lock():
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    except Exception:
        pass


# ---- index utils ----
def ensure_dirs():
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_index():
    ensure_dirs()
    if not INDEX_FILE.exists():
        return {"count": 0, "urls": {}}
    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_index(index):
    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)


# ---- normalization ----
def normalize_record(rec, source):
    # rec: dict minimal contenant au moins 'url' et 'title' / 'company'...
    r = {c: "" for c in UNIFIED_COLUMNS}
    r["source"] = source
    # Map common keys (adapter selon scrapers)
    r["title"] = rec.get("title", "") or rec.get("job_title", "")
    r["company"] = rec.get("company", "")
    r["region"] = rec.get("location", "") or rec.get("region", "")
    r["sector"] = rec.get("category", "") or rec.get("sector", "")
    r["short_description"] = rec.get("description", "")[:400] if rec.get("description") else ""
    r["full_description"] = rec.get("description", "") or rec.get("full_description", "")
    r["education"] = rec.get("education", "")
    r["experience"] = rec.get("experience", "")
    r["contract"] = rec.get("contract", "")
    r["skills"] = rec.get("skills", "")
    r["salary"] = rec.get("salary", "")
    r["date"] = rec.get("date", "")
    r["url"] = rec.get("url", "")
    return r


# ---- efficient trim using small memory footprint ----
def tail_rows_from_csv(path, n, chunksize=5000):
    """Retourne une list de dicts des dernières n lignes du CSV sans charger tout le fichier."""
    if n <= 0 or not Path(path).exists():
        return []
    dq = deque(maxlen=n)
    for chunk in pd.read_csv(path, dtype=str, chunksize=chunksize, encoding="utf-8-sig"):
        for _, row in chunk.iterrows():
            dq.append(row.to_dict())
    return list(dq)


# ---- append / write API ----
def append_records(records, source):
    """
    records: list[dict] (each must contain 'url' at least)
    Retourne un résumé: {'added': x, 'skipped': y, 'total': z}
    """
    ensure_dirs()
    if not records:
        return {"added": 0, "skipped": 0, "total": 0}

    acquire_lock()
    try:
        index = load_index()
        existing_urls = set(index.get("urls", {}).keys())

        # filter duplicates quickly
        new_recs = [r for r in records if r.get("url") and r.get("url") not in existing_urls]
        skipped = len(records) - len(new_recs)
        if not new_recs:
            return {"added": 0, "skipped": skipped, "total": index.get("count", 0)}

        # normalize
        normalized = [normalize_record(r, source) for r in new_recs]
        new_df = pd.DataFrame(normalized, columns=UNIFIED_COLUMNS)

        current_count = index.get("count", 0)
        will_total = current_count + len(new_df)

        if not OUTPUT_FILE.exists():
            # write fresh
            # assign job_id starting at 1
            new_df = new_df.reset_index(drop=True)
            new_df.index = new_df.index + 1
            new_df["job_id"] = new_df.index.astype(int)
            new_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
            # update index
            index["count"] = len(new_df)
            for _, row in new_df.iterrows():
                index.setdefault("urls", {})[row["url"]] = int(row["job_id"])
            save_index(index)
            return {"added": len(new_df), "skipped": skipped, "total": index["count"]}

        # if within limit, append fast
        if will_total <= MAX_JOBS:
            # assign job ids continuing from current_count
            start_id = current_count + 1
            new_df = new_df.reset_index(drop=True)
            new_df.index = new_df.index + start_id
            new_df["job_id"] = new_df.index.astype(int)
            # append without header
            new_df.to_csv(OUTPUT_FILE, mode="a", index=False, header=False, encoding="utf-8-sig")
            # update index
            for _, row in new_df.iterrows():
                index.setdefault("urls", {})[row["url"]] = int(row["job_id"])
            index["count"] = current_count + len(new_df)
            save_index(index)
            return {"added": len(new_df), "skipped": skipped, "total": index["count"]}

        # Else: need to trim oldest to keep MAX_JOBS.
        keep = MAX_JOBS - len(new_df)
        if keep < 0:
            # new batch alone exceeds MAX_JOBS: keep only last MAX_JOBS of new_df
            new_df = new_df.tail(MAX_JOBS).reset_index(drop=True)
            new_df.index = new_df.index + 1
            new_df["job_id"] = new_df.index.astype(int)
            # overwrite file
            new_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
            # rebuild index from new_df
            index = {"count": len(new_df), "urls": {row["url"]: int(row["job_id"]) for _, row in new_df.iterrows()}}
            save_index(index)
            return {"added": len(new_df), "skipped": skipped, "total": index["count"]}

        # keep > =0: keep last `keep` rows from existing CSV, then append new_df
        tail_rows = tail_rows_from_csv(OUTPUT_FILE, keep)
        # create DataFrame from tail rows (may need to ensure columns)
        if tail_rows:
            tail_df = pd.DataFrame(tail_rows)
            # ensure columns order
            tail_df = tail_df[UNIFIED_COLUMNS]
        else:
            tail_df = pd.DataFrame(columns=UNIFIED_COLUMNS)

        final_df = pd.concat([tail_df.reset_index(drop=True), new_df.reset_index(drop=True)], ignore_index=True, sort=False)
        # reassign job ids 1..len(final_df)
        final_df.index = final_df.index + 1
        final_df["job_id"] = final_df.index.astype(int)
        final_df = final_df[UNIFIED_COLUMNS]  # reorder

        # write atomically to temp then rename
        tmp = OUTPUT_FILE.with_suffix(".tmp.csv")
        final_df.to_csv(tmp, index=False, encoding="utf-8-sig")
        tmp.replace(OUTPUT_FILE)

        # rebuild index (cheap: it contains at most MAX_JOBS urls)
        index = {"count": len(final_df), "urls": {row["url"]: int(row["job_id"]) for _, row in final_df.iterrows()}}
        save_index(index)
        return {"added": len(new_df), "skipped": skipped, "total": index["count"]}

    finally:
        release_lock()
