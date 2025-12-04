import requests
from bs4 import BeautifulSoup
import csv
import time
import random

BASE_URL = "https://institutpf.org/repertoire?postalCode=&radius=&name=&domain=&page={}"
TOTAL_PAGES = 469

OUTPUT_FILE = "contacts.csv"


def debug(msg):
    """Global debug printer"""
    print(f"[DEBUG] {msg}")


def get_page(url):
    """Request a page with retry + debugging"""
    for attempt in range(1, 6):
        try:
            debug(f"Requesting URL: {url} (Attempt {attempt})")
            response = requests.get(url, timeout=10)

            debug(f"Status code: {response.status_code}")

            if response.status_code == 200:
                return response.text

            debug(f"Non-200 response: {response.status_code}")

        except Exception as e:
            debug(f"Request failed: {str(e)}")

        time.sleep(random.uniform(1, 3))

    debug("!!! FINAL FAILURE: Could not fetch page even after retries.")
    return None


def parse_card(card):
    """Extract fields safely with debug logs"""
    def safe_text(selector):
        tag = card.select_one(selector)
        if not tag:
            debug(f"Missing field for selector: {selector}")
            return ""
        return tag.get_text(strip=True)

    name = safe_text("h4 a")
    company = safe_text("h5")
    address = safe_text("p span")
    phone = safe_text("p a")

    debug(f"Extracted -> Name: {name}, Company: {company}, Address: {address}, Phone: {phone}")

    return [name, company, address, phone]


def scrape_page(page_no):
    url = BASE_URL.format(page_no)
    html = get_page(url)

    if not html:
        debug(f"Skipping page {page_no} due to load failure.")
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("li.find-pl-fin-tile")
    debug(f"Found {len(cards)} cards on page {page_no}")

    results = []

    for index, card in enumerate(cards):
        debug(f"Parsing card #{index + 1} on page {page_no}")
        results.append(parse_card(card))

    return results

def save_to_excel(csv_file, excel_file):
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)
    print(f"Excel file saved as: {excel_file}")

def main():
    debug("Starting scraping job...")
    all_data = []

    for page in range(1, TOTAL_PAGES + 1):
        debug(f"========================")
        debug(f"SCRAPING PAGE {page}/{TOTAL_PAGES}")
        debug(f"========================")

        page_data = scrape_page(page)
        all_data.extend(page_data)

        # avoid getting blocked
        sleep_time = random.uniform(1.5, 3.5)
        debug(f"Sleeping {sleep_time:.2f}s before next page...")
        time.sleep(sleep_time)

    # Save CSV
    debug("Saving data to CSV...")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Company", "Address", "Phone"])
        writer.writerows(all_data)
    
    save_to_excel(OUTPUT_FILE, "contacts.xlsx")

    debug(f"FINISHED! Total records saved: {len(all_data)}")


if __name__ == "__main__":
    main()
