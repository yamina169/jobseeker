# -*- coding: utf-8 -*-
"""
forjobscraper_fast.py
Scraper Farojob par catégorie optimisé avec récupération parallèle des descriptions
et gestion CSV avec limite globale et limite par secteur.
Optimisé pour vitesse : plus de Selenium, plus de parallélisme.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

import time
import random
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import pandas as pd

# ---------- CONFIG ----------
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "offres_brutes/farojob.csv"

MAX_WORKERS = 16          # plus de threads pour parallélisme
REQUEST_TIMEOUT = 5
RATE_MIN, RATE_MAX = 0.05, 0.1
MAX_TOTAL_JOBS = 500      # limite totale dans le CSV

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")
HEADERS = {"User-Agent": USER_AGENT}
SESSION = requests.Session()
SESSION.headers.update(HEADERS)

# ---------- CATEGORIES ----------
CATEGORIES = [
    "administratif",
    "architecture", "audiovisuel",
    "banque", "biologie", "call-center",
    "commerce", "comptabilite",
    "cosmetique", "droit",  "energie",
    "enseignement", "finance", "formation", "genie-civil",
    "genie-electrique", "immobilier", "informatique"
]
SECTOR_LIMITS = {cat: 1 for cat in CATEGORIES}
SECTOR_LIMITS["informatique"] = 1
# ---------- UTIL ----------
def random_sleep(a=RATE_MIN, b=RATE_MAX):
    time.sleep(random.uniform(a, b))

def category_page_url(category, page):
    return f"https://www.farojob.net/jobs/?s&category[0]={category}&paged={page}"

# ---------- Parsers ----------
def parse_farojob_list(html):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select(".loop-item-wrap.list")
    results = []
    for c in cards:
        title_el = c.select_one("h3.loop-item-title a")
        title = title_el.get_text(strip=True) if title_el else "N/A"
        link = title_el["href"] if title_el and title_el.has_attr("href") else None
        company_el = c.select_one(".job-company span")
        company = company_el.get_text(strip=True) if company_el else "N/A"
        location_el = c.select_one(".job-location em")
        location = location_el.get_text(strip=True) if location_el else "N/A"
        date_posted_el = c.select_one(".job-date__posted")
        date_posted = date_posted_el.get_text(strip=True) if date_posted_el else "N/A"
        results.append({
            "title": title,
            "company": company,
            "location": location,
            "date_posted": date_posted,
            "url": link
        })
    return results

def parse_farojob_detail(html):
    soup = BeautifulSoup(html, "lxml")
    desc_el = soup.select_one("div.job-desc[itemprop='description']")
    return {"description": " ".join(desc_el.stripped_strings) if desc_el else "N/A"}

def fetch_url(url):
    try:
        resp = SESSION.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return None

def fetch_job_details_parallel(records):
    def fetch(rec):
        url = rec.get("url")
        if not url:
            rec["description"] = "N/A"
            return rec
        html = fetch_url(url)
        rec["description"] = parse_farojob_detail(html or "").get("description", "N/A")
        random_sleep()
        return rec

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(fetch, rec) for rec in records]
        for f in as_completed(futures):
            results.append(f.result())
    return results

# ---------- CSV utils ----------
def load_existing_jobs():
    jobs = []
    existing_urls = set()
    if OUTPUT_FILE.exists():
        df = pd.read_csv(OUTPUT_FILE)
        jobs = df.to_dict(orient="records")
        existing_urls = set(df["url"].tolist())
    return jobs, existing_urls

def save_jobs(all_jobs):
    if len(all_jobs) > MAX_TOTAL_JOBS:
        all_jobs = all_jobs[-MAX_TOTAL_JOBS:]
    for idx, job in enumerate(all_jobs, start=1):
        job["job_id"] = idx
    df = pd.DataFrame(all_jobs)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")
    print(f"{len(all_jobs)} jobs sauvegardés dans {OUTPUT_FILE}")

# ---------- Scraper principal ----------
def scrape_farojob_categories():
    all_jobs, existing_urls = load_existing_jobs()
    sector_counts = {cat: 0 for cat in CATEGORIES}

    for cat in CATEGORIES:
        print(f"\n=== Scraping category: {cat} ===")
        page = 1
        while sector_counts[cat] < SECTOR_LIMITS[cat]:
            url = category_page_url(cat, page)
            items = fetch_url(url)
            if not items:
                break
            items = parse_farojob_list(items)
            new_items = [i for i in items if i.get("url") not in existing_urls]
            if not new_items:
                break
            # Récupérer détails en parallèle
            new_items = fetch_job_details_parallel(new_items)
            for rec in new_items:
                if sector_counts[cat] >= SECTOR_LIMITS[cat]:
                    break
                rec["category"] = cat
                all_jobs.append(rec)
                existing_urls.add(rec["url"])
                sector_counts[cat] += 1
            page += 1
            random_sleep()

    save_jobs(all_jobs)
    return all_jobs

# ---------- Main ----------
if __name__ == "__main__":
    start = time.time()
    items = scrape_farojob_categories()
    duration = time.time() - start
    print("Done in %.2f seconds" % duration)
