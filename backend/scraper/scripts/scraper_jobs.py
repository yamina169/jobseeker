# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import csv
import time
import random
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# ✅ chemin du driver local
DRIVER_PATH = r"C:\\tools\\chromedriver\\chromedriver-win64\\chromedriver.exe"

HEADLESS = True
BASE_WAIT = 15
OUTPUT_DIR = Path("data/offres_brutes")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def make_driver():
    options = webdriver.ChromeOptions()
    if HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1366,768")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    )
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # ⚙️ utilisation du chemin local
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver


def random_sleep(a=1.0, b=2.5):
    time.sleep(random.uniform(a, b))
def scrape_emploitunisie(driver, pages=4):
    print("=== Emploitunisie ===")
    base = "https://www.emploitunisie.com/recherche-jobs-tunisie?page={}"
    results = []
    wait = WebDriverWait(driver, BASE_WAIT)

    for p in range(1, pages+1):
        url = base.format(p)
        print("page", p, url)
        driver.get(url)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.card.card-job")))
        except Exception:
            print(" Element list not found quickly on Emploitunisie")
            time.sleep(2)

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.card.card-job")
        print("found", len(job_cards), "items")
        
        for card in job_cards:
            try:
                title_el = card.find_element(By.CSS_SELECTOR, "div.card-job-detail h3 a")
                title = title_el.text.strip()
                link = title_el.get_attribute("href")
            except:
                title = "N/A"
                link = None

            try:
                company = card.find_element(By.CSS_SELECTOR, "a.card-job-company").text.strip()
            except:
                company = "N/A"

            try:
                description = card.find_element(By.CSS_SELECTOR, "div.card-job-description p").text.strip()
            except:
                description = "N/A"

            # Liste des informations supplémentaires
            try:
                edu = card.find_element(By.XPATH, ".//li[contains(text(),'Niveau d´études requis')]/strong").text.strip()
            except:
                edu = "N/A"

            try:
                experience = card.find_element(By.XPATH, ".//li[contains(text(),'Niveau d'expérience')]/strong").text.strip()
            except:
                experience = "N/A"

            try:
                contract = card.find_element(By.XPATH, ".//li[contains(text(),'Contrat proposé')]/strong").text.strip()
            except:
                contract = "N/A"

            try:
                region = card.find_element(By.XPATH, ".//li[contains(text(),'Région de')]/strong").text.strip()
            except:
                region = "N/A"

            try:
                skills = card.find_element(By.XPATH, ".//li[contains(text(),'Compétences clés')]/strong").text.strip()
            except:
                skills = "N/A"

            try:
                date = card.find_element(By.TAG_NAME, "time").get_attribute("datetime")
            except:
                date = "N/A"

            try:
                logo = card.find_element(By.CSS_SELECTOR, "picture img").get_attribute("src")
            except:
                logo = None

            results.append({
                "source": "Emploitunisie",
                "title": title,
                "company": company,
                "description": description,
                "education": edu,
                "experience": experience,
                "contract": contract,
                "region": region,
                "skills": skills,
                "date": date,
                "url": link,
                "logo": logo
            })

        time.sleep(1.0 + 1.2 * p)
    return results




# -----------------------------
# tunijobs scraper
# -----------------------------
def scrape_tunijobs(driver, pages=4):
    print("=== TuniJobs ===")
    base = "https://www.tunijobs.com/jobs?page={}"
    results = []
    wait = WebDriverWait(driver, BASE_WAIT)

    for p in range(1, pages+1):
        url = base.format(p)
        print("page", p, url)
        driver.get(url)

        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.p-6.flex.flex-col.h-full")))
        except Exception:
            print("Job cards not found quickly on TuniJobs")
            random_sleep(1.5,2.5)

        cards = driver.find_elements(By.CSS_SELECTOR, "div.p-6.flex.flex-col.h-full")
        print("found", len(cards), "items")

        for c in cards:
            # Titre et lien
            try:
                title_el = c.find_element(By.CSS_SELECTOR, "div.flex.items-start.gap-4.mb-4 h3")
                title = title_el.text.strip()
                link = c.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")
            except:
                title, link = "N/A", None

            # Entreprise
            try:
                company = c.find_element(By.CSS_SELECTOR, "div.flex.items-start.gap-4.mb-4 + div").text.strip()
            except:
                company = "N/A"

            # Logo
            try:
                logo = c.find_element(By.CSS_SELECTOR, "div.relative.bg-white img").get_attribute("src")
            except:
                logo = None

            # Expérience
            try:
                experience = c.find_element(By.XPATH, ".//div[p/text()='Expérience']/p[2]").text.strip()
            except:
                experience = "N/A"

            # Type d'emploi
            try:
                job_type = c.find_element(By.XPATH, ".//div[p/text()='Type d'emploi']/p[2]").text.strip()
            except:
                job_type = "N/A"

            # Mode de travail
            try:
                work_mode = c.find_element(By.XPATH, ".//div[p/text()='Mode de travail']/p[2]").text.strip()
            except:
                work_mode = "N/A"

            # Rémunération
            try:
                salary = c.find_element(By.XPATH, ".//div[p/text()='Rémunération']/p[2]").text.strip()
            except:
                salary = "N/A"

            # Compétences
            try:
                skills = c.find_element(By.CSS_SELECTOR, "div.flex.flex-wrap.gap-1").text.strip()
            except:
                skills = "N/A"

            # Dates
            try:
                published = c.find_element(By.XPATH, ".//div[contains(text(),'Publié:')]/span").text.strip()
            except:
                published = "N/A"

            try:
                modified = c.find_element(By.XPATH, ".//div[contains(text(),'Modifié:')]/span").text.strip()
            except:
                modified = "N/A"

            results.append({
                "source": "TuniJobs",
                "title": title,
                "company": company,
                "logo": logo,
                "experience": experience,
                "job_type": job_type,
                "work_mode": work_mode,
                "salary": salary,
                "skills": skills,
                "published": published,
                "modified": modified,
                "url": link
            })

        random_sleep(1.0,2.0)

    return results

# -----------------------------
# Farojob scraper
# -----------------------------
def scrape_farojob(driver, pages=4):
    print("=== Farojob ===")
    base = "https://www.farojob.net/jobs?page={}"
    results = []
    wait = WebDriverWait(driver, 10)

    for p in range(1, pages + 1):
        url = base.format(p)
        print("page", p, url)
        driver.get(url)

        try:
            wait.until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".loop-item-wrap.list")
            ))
        except Exception:
            print("Aucune offre trouvée sur la page", p)
            continue

        cards = driver.find_elements(By.CSS_SELECTOR, ".loop-item-wrap.list")
        print("found", len(cards), "items")

        for c in cards:
            # Titre et lien
            try:
                title_el = c.find_element(By.CSS_SELECTOR, "h3.loop-item-title a")
                title = title_el.text.strip()
                link = title_el.get_attribute("href")
            except:
                title, link = "N/A", None

            # Entreprise
            try:
                company_el = c.find_element(By.CSS_SELECTOR, ".job-company span")
                company = company_el.text.strip()
            except:
                company = "N/A"

            # Logo
            try:
                logo = c.find_element(By.CSS_SELECTOR, ".item-featured a img").get_attribute("src")
            except:
                logo = None

            # Location
            try:
                location = c.find_element(By.CSS_SELECTOR, ".job-location em").text.strip()
            except:
                location = "N/A"

            # Type d'emploi
            try:
                job_type = c.find_element(By.CSS_SELECTOR, ".job-type span").text.strip()
            except:
                job_type = "N/A"

            # Date absolue
            try:
                date_posted = c.find_element(By.CSS_SELECTOR, ".job-date__posted").text.strip()
            except:
                date_posted = "N/A"

            # Date relative (ex: il y a 5 mois)
            try:
                date_ago = c.find_element(By.CSS_SELECTOR, ".job-date-ago").text.strip()
            except:
                date_ago = "N/A"

            # Lien "Voir plus"
            try:
                see_more = c.find_element(By.CSS_SELECTOR, ".show-view-more a.btn").get_attribute("href")
            except:
                see_more = None

            results.append({
                "source": "Farojob",
                "title": title,
                "company": company,
                "logo": logo,
                "location": location,
                "job_type": job_type,
                "date_posted": date_posted,
                "date_ago": date_ago,
                "url": link,
                "see_more": see_more
            })

    return results

# -----------------------------
# Helper to save results
# -----------------------------
def save_results(records, filename):
    if not records:
        print("Aucun enregistrement pour", filename)
        return
    df = pd.DataFrame(records)
    out = OUTPUT_DIR / filename
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"{len(records)} enregistrements sauvegardés dans {out}")

# -----------------------------
# Main
# -----------------------------
def main():
    driver = make_driver()
    try:
        all_results = []

        # adapte le nombre de pages selon besoin
        em = scrape_emploitunisie(driver, pages=4)
        save_results(em, "emploitunisie.csv")
        all_results += em

        tj = scrape_tunijobs(driver, pages=4)
        save_results(tj, "tunijobs.csv")
        all_results += tj



        fj = scrape_farojob(driver, pages=4)
        save_results(fj, "farojob.csv")
        all_results += fj

        # sauvegarde globale
        save_results(all_results, "all_jobs_combined.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()