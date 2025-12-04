# Web Scraper – Usage & Debugging Guide

This script scrapes contact information (Name, Company, Address, Phone) from a multi-page directory website(https://institutpf.org/repertoire?postalCode=&radius=&name=&domain=&page=1) (1–469 pages) and saves the results to CSV and Excel files.

This README explains:
- How to run the script
- What files it generates
- How to debug common issues

---

## 🚀 How to Use

### 1. Install dependencies

```
pip install -r requirements.txt
```

Your requirements.txt should contain:

```
requests
beautifulsoup4
lxml
pandas
openpyxl
```

---

### 2. Run the scraper

```
python scraper.py
```

After running successfully, the script generates:

- contacts.csv
- contacts.xlsx

Both files include:

- Name
- Company
- Address
- Phone

---

## 📁 Output Files

CSV file:
```
contacts.csv
```

Excel file:
```
contacts.xlsx
```

---

## 🪲 Simple Debugging Guide

### 1. If the page fails to load

```
[DEBUG] Request failed: ...
[DEBUG] Retrying (Attempt 2)...
```

The script retries automatically up to 5 times.

---

### 2. If no cards are found

```
[DEBUG] Found 0 cards on page 10
```

Possible reasons:
- Wrong selector
- Website changed structure
- Request blocked

Fix the card selector:
```
cards = soup.select("li.find-pl-fin-tile")
```

---

### 3. If a field is missing

```
[DEBUG] Missing field for selector: p span
```

Selectors may need updating:
```
name    = card.select_one("h4 a")
company = card.select_one("h5")
address = card.select_one("p span")
phone   = card.select_one("p a")
```

---

### 4. If Excel fails to save

Install:
```
pip install pandas openpyxl
```

---

## ✔ Successful Run Example

```
[DEBUG] Found 12 cards on page 15
[DEBUG] Extracted -> Name: Jane Doe | Company: XYZ Ltd | Phone: 514-123-4567
[DEBUG] Saving contacts.csv...
[DEBUG] Creating contacts.xlsx...
[DEBUG] Done!
```

---

## 📌 Notes

- Avoid running too fast to prevent blocking.
- HTML changes require selector changes.
- Debug logs always show the exact problem.

---

## 📞 Help

If the script breaks, share one card’s HTML to fix selectors.
