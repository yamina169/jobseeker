# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
from urllib.parse import urljoin

# -----------------------------
# Config
# -----------------------------
BASE_LIST_URL = "https://www.emploitunisie.com/recherche-jobs-tunisie/{}?page={}"
BASE_DOMAIN = "https://www.emploitunisie.com"
OUTPUT_DIR = Path("data/offres_brutes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "emploitunisie.csv"

HEADERS = {"User-Agent": "Mozilla/5.0"}
REQ_TIMEOUT = 10  # seconds

# Mapping des catégories Emploitunisie → mots-clés
JOB_CATEGORIES = {
    "Informatique, nouvelles technologies": "informatique",
    "Télémarketing, téléassistance": "telemarketing",
    "Gestion, comptabilité, finance": "finance",
    "Commercial, vente": "vente",
    "Métiers de la santé et du social": "sante",
}

# Regroupement en 3 secteurs principaux
MAIN_SECTORS = {
    "IT": ["Informatique, nouvelles technologies"],
    "Management": ["Management, direction générale", "Juridique", "RH, formation"],
    "Commercial": [
        "Commercial, vente",
        "Achats",
        "Gestion, comptabilité, finance",
        "Marketing, communication",
        "Télémarketing, téléassistance",
        "Secrétariat, assistanat",
        "Tourisme, hôtellerie, restauration",
        "Transport, logistique",
        "Métiers de la santé et du social",
        "Métiers des services",
        "Métiers du BTP",
        "Production, maintenance, qualité"
    ]
}

MAX_JOBS_PER_CATEGORY = 1
MAX_TOTAL = 500
MAX_WORKERS = 8
POLL_SLEEP = (0.2, 0.3)


# -----------------------------
# Helpers
# -----------------------------
def txt(el):
    return el.get_text(strip=True) if el else ""

def abs_url(href):
    if not href:
        return ""
    return href if href.startswith("http") else urljoin(BASE_DOMAIN, href)

def map_to_main_sector(sector_name):
    for main, sub_list in MAIN_SECTORS.items():
        for sub in sub_list:
            if sub.lower() in sector_name.lower():
                return main
    return "Autre"


# -----------------------------
# Parsing
# -----------------------------
def parse_list_card(card):
    title_el = card.select_one("div.card-job-detail h3 a")
    title = txt(title_el)
    url = abs_url(title_el["href"]) if title_el and title_el.has_attr("href") else ""
    company = txt(card.select_one("a.card-job-company"))
    description = txt(card.select_one("div.card-job-description p"))

    education = "N/A"
    experience = "N/A"
    contract = "N/A"
    region = "N/A"
    skills = "N/A"

    for li in card.select("li"):
        text = txt(li).lower()
        s = li.find("strong")
        val = txt(s) if s else txt(li)
        if "études" in text or "niveau d" in text:
            education = val
        if "expérience" in text:
            experience = val
        if "contrat" in text:
            contract = val
        if "région" in text or "lieu" in text:
            region = val
        if "compétences" in text:
            skills = val

    date = "N/A"
    time_el = card.find("time")
    if time_el and time_el.has_attr("datetime"):
        date = time_el["datetime"]

    return {
        "title": title,
        "company": company,
        "description": description,
        "education": education,
        "experience": experience,
        "contract": contract,
        "region": region,
        "skills": skills,
        "date": date,
        "url": url,
    }


def fetch_list_page(session, keyword, page):
    url = BASE_LIST_URL.format(keyword, page)
    r = session.get(url, headers=HEADERS, timeout=REQ_TIMEOUT)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select("div.card.card-job")


def fetch_job_detail(session, job):
    job_url = job.get("url", "")
    job["full_description"] = ""
    if not job_url:
        return job
    try:
        r = session.get(job_url, headers=HEADERS, timeout=REQ_TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        el = soup.select_one("div.job-description") or soup.select_one(".job-description") or soup.select_one(".prose")
        job["full_description"] = txt(el) if el else ""
    except Exception:
        job["full_description"] = ""
    return job


# -----------------------------
# CSV utilities
# -----------------------------
def load_existing_jobs():
    jobs = []
    existing_urls = set()
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(row)
                existing_urls.add(row.get("url", ""))
    return jobs, existing_urls


def save_jobs(jobs):
    if len(jobs) > MAX_TOTAL:
        jobs = jobs[-MAX_TOTAL:]
    for i, j in enumerate(jobs, start=1):
        j["job_id"] = str(i)
        j["source"] = "Emploitunisie"
    fieldnames = ["job_id", "source", "sector", "title", "company", "description", "full_description",
                  "education", "experience", "contract", "region", "skills", "date", "url"]
    for job in jobs:
        for k in fieldnames:
            if k not in job:
                job[k] = ""
    with open(OUTPUT_FILE, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)
    print(f"✔ {len(jobs)} jobs sauvegardés dans {OUTPUT_FILE}")


# -----------------------------
# Core scraping logic
# -----------------------------
def scrape_category_fast(session, keyword, category_name, existing_urls):
    new_jobs = []
    page = 1
    while len(new_jobs) < MAX_JOBS_PER_CATEGORY:
        try:
            cards = fetch_list_page(session, keyword, page)
        except Exception as e:
            print(f"[WARN] erreur page {page} ({keyword}): {e}")
            break
        if not cards:
            break

        for card in cards:
            if len(new_jobs) >= MAX_JOBS_PER_CATEGORY:
                break
            base = parse_list_card(card)
            url = base.get("url", "")
            if not url or url in existing_urls:
                continue
            # Mapper vers secteur principal
            base["sector"] = map_to_main_sector(category_name)
            new_jobs.append(base)
            existing_urls.add(url)

        page += 1
        time.sleep(random.uniform(*POLL_SLEEP))

    if not new_jobs:
        print(f"→ 0 nouveaux jobs pour {category_name}")
        return []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(fetch_job_detail, session, job) for job in new_jobs]
        detailed = []
        for f in as_completed(futures):
            detailed.append(f.result())

    print(f"→ {len(detailed)} nouveaux jobs récupérés pour {category_name}")
    return detailed


def main():
    start = time.time()
    session = requests.Session()
    session.headers.update(HEADERS)

    all_jobs, existing_urls = load_existing_jobs()
    print(f"Chargé {len(all_jobs)} jobs existants (CSV).")

    added = 0
    for cat_name, kw in JOB_CATEGORIES.items():
        needed_before = sum(1 for j in all_jobs if j.get("sector") == map_to_main_sector(cat_name))
        print(f"\n[Catégorie] {cat_name} (déjà {needed_before} dans CSV) — récupération jusqu'à {MAX_JOBS_PER_CATEGORY} nouveaux...")
        new = scrape_category_fast(session, kw, cat_name, existing_urls)
        if new:
            all_jobs.extend(new)
            added += len(new)

    save_jobs(all_jobs)
    elapsed = time.time() - start
    print(f"Terminé — {added} nouveau(x) job(s) ajoutés. Temps: {elapsed:.1f}s")


if __name__ == "__main__":
    main()
