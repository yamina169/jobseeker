import sys
sys.stdout.reconfigure(encoding='utf-8')

import requests
from bs4 import BeautifulSoup
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://www.keejob.com/offres-emploi/?page={}"
OUTPUT_DIR = Path("data/offres_brutes")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_FILE = OUTPUT_DIR / "keejob.csv"

HEADERS = {"User-Agent": "Mozilla/5.0"}

# -------------------------------
# Top 5 secteurs
# -------------------------------
TOP_SECTORS = {
    "informatique / télécoms": "23",
    "call center / télévente": "7",
    "comptabilité / gestion / audit / finance / banque": "6",
    "commerce / vente / distribution": "9",
    "santé / paramédical / optique": "26"
}

MAX_JOBS = {
    "informatique / télécoms": 20,
    "call center / télévente": 5,
    "comptabilité / gestion / audit / finance / banque": 5,
    "commerce / vente / distribution": 5,
    "santé / paramédical / optique": 5
}

# -------------------------------
# Utilitaires
# -------------------------------
def txt(e):
    return e.get_text(strip=True) if e else ""

def parse_job_card(card):
    title_el = card.select_one("h2 a")
    title = txt(title_el)
    url = "https://www.keejob.com" + title_el["href"] if title_el else ""

    company = txt(card.select_one("p a"))
    short_desc = txt(card.select_one("div.mb-3 p"))

    reg_icon = card.select_one("i.fa-map-marker-alt")
    region = txt(reg_icon.find_next("span")) if reg_icon else ""

    date_icon = card.select_one("i.fa-clock")
    date = txt(date_icon.find_next("span")) if date_icon else ""

    contract = ""
    for tag in card.select("div.flex.flex-wrap span"):
        t = txt(tag).lower()
        if "cdi" in t or "cdd" in t or "contrat" in t:
            contract = txt(tag)

    return {
        "title": title,
        "company": company,
        "short_description": short_desc,
        "region": region,
        "date": date,
        "contract": contract,
        "url": url,
    }

def parse_job_details(session, url):
    r = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    details = {
        "full_description": "",
        "education": "",
        "experience": "",
        "salary": "",
        "contract": "",
        "region": "",
    }
    details["full_description"] = txt(soup.select_one(".prose"))
    for block in soup.select(".p-6 div"):
        label = txt(block.select_one("h3")).lower()
        value = txt(block.select_one("p")) or txt(block.select_one("span"))
        if "contrat" in label:
            details["contract"] = value
        elif "études" in label or "education" in label:
            details["education"] = value
        elif "expérience" in label:
            details["experience"] = value
        elif "salaire" in label:
            details["salary"] = value
        elif "lieu" in label or "région" in label:
            details["region"] = value
    return details

def get_job_cards(session, page, sector_id=None):
    url = BASE_URL.format(page)
    if sector_id:
        url += f"&industries[]={sector_id}"
    r = session.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.select("div.flex-1.min-w-0")

def scrape_job(session, base, sector_name, job_id):
    try:
        details = parse_job_details(session, base["url"])
        return {**base, **details, "sector": sector_name, "job_id": job_id}
    except Exception as e:
        print(f"[ERREUR] {base.get('url', '')}: {e}")
        return None

# -------------------------------
# MAIN
# -------------------------------
def main():
    print("\n=== SCRAPING KEEJOB (TOP SECTORS) ===\n")

    jobs = []
    job_counter = 1

    # Lire jobs existants
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                jobs.append(row)
            if jobs:
                job_counter = max(int(j.get("job_id", 0)) for j in jobs) + 1

    session = requests.Session()

    for sector_name, sector_id in TOP_SECTORS.items():
        max_jobs = MAX_JOBS[sector_name]
        scraped_count = 0
        page = 1
        print(f"\n--- Scraping secteur: {sector_name} (max {max_jobs} jobs) ---\n")

        while scraped_count < max_jobs:
            cards = get_job_cards(session, page, sector_id)
            if not cards:
                break
            print(f"Page {page} -> {len(cards)} offres trouvées")

            # Préparer jobs uniques
            to_scrape = []
            for card in cards:
                base = parse_job_card(card)
                if not base["url"]:
                    continue
                if any(j["url"] == base["url"] for j in jobs):
                    continue
                to_scrape.append((base, job_counter))
                job_counter += 1

            # Scraper en parallèle
            with ThreadPoolExecutor(max_workers=8) as executor:
                futures = [executor.submit(scrape_job, session, base, sector_name, jid) for base, jid in to_scrape]
                for future in as_completed(futures):
                    job = future.result()
                    if job:
                        jobs.append(job)
                        scraped_count += 1
                        if scraped_count >= max_jobs:
                            break

            if scraped_count >= max_jobs:
                break
            page += 1

    # Limiter à 500 jobs max
    if len(jobs) > 500:
        jobs = jobs[-500:]

    # Sauvegarder CSV
    if jobs:
        with open(OUTPUT_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(jobs[0].keys()))
            writer.writeheader()
            writer.writerows(jobs)
        print(f"\n✔ Terminé : {len(jobs)} offres sauvegardées dans {OUTPUT_FILE} (max 500)")
    else:
        print("\n⚠ Aucun job récupéré.")

if __name__ == "__main__":
    main()
