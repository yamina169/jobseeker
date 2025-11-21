# fast_scraper.py
# Python 3.8+
import time
import random
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ---------- CONFIG ----------
DRIVER_PATH = r"C:\\tools\\chromedriver\\chromedriver-win64\\chromedriver.exe"
HEADLESS = True
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_WORKERS = 6           # threads pour requests (ajuster selon CPU / réseau)
PAGE_CONCURRENCY = 4      # pages parallèles par site
REQUEST_TIMEOUT = 12      # secondes
RATE_MIN, RATE_MAX = 0.3, 1.0  # pause aléatoire entre requêtes

USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36")

headers = {"User-Agent": USER_AGENT}
session = requests.Session()
session.headers.update(headers)

# ---------- UTIL ----------
def random_sleep(a=RATE_MIN, b=RATE_MAX):
    time.sleep(random.uniform(a, b))

def save_results(records, filename):
    if not records:
        print("No records for", filename)
        return
    df = pd.DataFrame(records)
    out = OUTPUT_DIR / filename
    df.to_csv(out, index=False, encoding="utf-8-sig")
    print(f"{len(records)} records saved to {out}")

# ---------- Selenium fallback (only used if needed) ----------
def make_selenium_driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1366,768")
    opts.add_argument(f"user-agent={USER_AGENT}")
    service = Service(DRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=opts)
    # hide webdriver flag
    try:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    except Exception:
        pass
    return driver

def fetch_with_selenium(url, driver, wait_seconds=8):
    driver.get(url)
    time.sleep(min(wait_seconds, 3))  # give it some time; keep short
    return driver.page_source

# ---------- Parsers (BS4) ----------
# Each parser tries to extract the same fields as your original script.
# They rely on the page HTML structure; if structure changes adapt selectors.

def parse_emploitunisie_list(html):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("div.card.card-job")
    results = []
    for card in cards:
        try:
            title_el = card.select_one("div.card-job-detail h3 a")
            title = title_el.get_text(strip=True) if title_el else "N/A"
            link = title_el["href"] if title_el and title_el.has_attr("href") else None
        except:
            title, link = "N/A", None
        company = card.select_one("a.card-job-company")
        company = company.get_text(strip=True) if company else "N/A"
        description = card.select_one("div.card-job-description p")
        description = description.get_text(strip=True) if description else "N/A"

        def safe_xpath_text(sel):
            try:
                node = sel
                return node.get_text(strip=True) if node else "N/A"
            except:
                return "N/A"

        # fallback selectors using text matching where possible
        def find_li_strong(containing):
            li = card.find("li", string=lambda s: s and containing in s)
            if li:
                strong = li.find("strong")
                return strong.get_text(strip=True) if strong else "N/A"
            return "N/A"

        edu = find_li_strong('Niveau d´études requis') or find_li_strong('Niveau d’études requis')
        experience = find_li_strong("Niveau d'expérience")
        contract = find_li_strong("Contrat proposé")
        region = find_li_strong("Région")
        skills = find_li_strong("Compétences")
        time_tag = card.find("time")
        date = time_tag["datetime"] if time_tag and time_tag.has_attr("datetime") else "N/A"
        logo_el = card.select_one("picture img")
        logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else None

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
    return results

def parse_tunijobs_list(html):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select("div.p-6.flex.flex-col.h-full")
    results = []
    for c in cards:
        try:
            title_el = c.select_one("div.flex.items-start.gap-4.mb-4 h3")
            title = title_el.get_text(strip=True) if title_el else "N/A"
            link_a = c.find("a", href=True)
            link = link_a["href"] if link_a else None
        except:
            title, link = "N/A", None
        # company fallback
        company = "N/A"
        try:
            sibling = c.select_one("div.flex.items-start.gap-4.mb-4 + div")
            if sibling:
                company = sibling.get_text(strip=True)
        except:
            company = "N/A"
        logo_el = c.select_one("div.relative.bg-white img")
        logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else None

        def safe_text(sel):
            try:
                return sel.get_text(strip=True)
            except:
                return "N/A"

        experience = safe_text(c.find(lambda tag: tag.name=="div" and tag.find("p") and "Expérience" in tag.text) or None)
        job_type = safe_text(c.find(lambda tag: tag.name=="div" and tag.find("p") and "Type d'emploi" in tag.text) or None)
        work_mode = safe_text(c.find(lambda tag: tag.name=="div" and tag.find("p") and "Mode de travail" in tag.text) or None)
        salary = safe_text(c.find(lambda tag: tag.name=="div" and tag.find("p") and "Rémunération" in tag.text) or None)
        skills_el = c.select_one("div.flex.flex-wrap.gap-1")
        skills = skills_el.get_text(" ", strip=True) if skills_el else "N/A"
        published = "N/A"
        modified = "N/A"
        # attempt to find published/modified spans
        sp_p = c.find(lambda t: t.name=="div" and "Publié" in t.text)
        if sp_p:
            span = sp_p.find("span")
            if span:
                published = span.get_text(strip=True)
        sp_m = c.find(lambda t: t.name=="div" and "Modifié" in t.text)
        if sp_m:
            span = sp_m.find("span")
            if span:
                modified = span.get_text(strip=True)

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
    return results

def parse_farojob_list(html):
    soup = BeautifulSoup(html, "lxml")
    cards = soup.select(".loop-item-wrap.list")
    results = []
    for c in cards:
        try:
            title_el = c.select_one("h3.loop-item-title a")
            title = title_el.get_text(strip=True) if title_el else "N/A"
            link = title_el["href"] if title_el and title_el.has_attr("href") else None
        except:
            title, link = "N/A", None
        company_el = c.select_one(".job-company span")
        company = company_el.get_text(strip=True) if company_el else "N/A"
        logo_el = c.select_one(".item-featured a img")
        logo = logo_el["src"] if logo_el and logo_el.has_attr("src") else None
        location = c.select_one(".job-location em")
        location = location.get_text(strip=True) if location else "N/A"
        job_type = c.select_one(".job-type span")
        job_type = job_type.get_text(strip=True) if job_type else "N/A"
        date_posted = c.select_one(".job-date__posted")
        date_posted = date_posted.get_text(strip=True) if date_posted else "N/A"
        date_ago = c.select_one(".job-date-ago")
        date_ago = date_ago.get_text(strip=True) if date_ago else "N/A"
        see_more = None
        sm_el = c.select_one(".show-view-more a.btn")
        if sm_el and sm_el.has_attr("href"):
            see_more = sm_el["href"]

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

# ---------- Combined worker that tries requests first ----------
def fetch_and_parse_list(url, parser, selenium_driver=None):
    """
    Try to fetch page with requests. If content doesn't contain expected markers,
    fallback to selenium_driver (if provided).
    """
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        html = resp.text
    except Exception as e:
        print("requests failed for", url, "->", e)
        html = None

    # quick heuristic: if HTML is None or doesn't include a marker we expect, fallback
    if not html or ("<html" not in html) or ("card-job" in parser.__name__ and "card-job" not in html and selenium_driver):
        print("falling back to selenium for", url)
        html = fetch_with_selenium(url, selenium_driver) if selenium_driver else html

    # parse
    try:
        return parser(html)
    except Exception as e:
        print("parsing failed for", url, "->", e)
        return []

# ---------- Site-specific orchestrators (parallel per page) ----------
def scrape_site_pages(base_url_template, pages, parser, selenium_driver=None):
    results = []
    # prepare page urls
    urls = [base_url_template.format(p) for p in range(1, pages+1)]
    with ThreadPoolExecutor(max_workers=min(MAX_WORKERS, len(urls))) as ex:
        future_to_url = {ex.submit(fetch_and_parse_list, url, parser, selenium_driver): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                items = future.result()
                print(f"parsed {len(items)} items from {url}")
                results.extend(items)
            except Exception as e:
                print("error fetching", url, e)
            random_sleep()
    return results

# ---------- High-level scrapers ----------
def scrape_all(pages_per_site=4, use_selenium_for_fallback=True):
    # create single selenium driver only if fallback needed
    driver = make_selenium_driver() if use_selenium_for_fallback else None
    all_results = []

    try:
        em_base = "https://www.emploitunisie.com/recherche-jobs-tunisie?page={}"
        em = scrape_site_pages(em_base, pages_per_site, parse_emploitunisie_list, driver)
        save_results(em, "emploitunisie.csv")
        all_results += em

        tj_base = "https://www.tunijobs.com/jobs?page={}"
        tj = scrape_site_pages(tj_base, pages_per_site, parse_tunijobs_list, driver)
        save_results(tj, "tunijobs.csv")
        all_results += tj

        fj_base = "https://www.farojob.net/jobs?page={}"
        fj = scrape_site_pages(fj_base, pages_per_site, parse_farojob_list, driver)
        save_results(fj, "farojob.csv")
        all_results += fj

        save_results(all_results, "all_jobs_combined.csv")
    finally:
        if driver:
            driver.quit()

# ---------- Main ----------
if __name__ == "__main__":
    start = time.time()
    scrape_all(pages_per_site=4, use_selenium_for_fallback=True)
    duration = time.time() - start
    print("Done in %.2f seconds" % duration)
