import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
DEFAULT_URL = os.getenv("DEFAULT_DASHEN_URL")

def scrape_dashen_bank(url=DEFAULT_URL):
    """
    Scrape the Dashen Bank exchange rates.
    """
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "html.parser")

        cash_tabs = soup.find("div", class_="et_pb_tab_0")
        transaction_tabs = soup.find("div", class_="et_pb_tab_1")

        cash_tbody = cash_tabs.find("tbody")
        cash_rows = cash_tbody.find_all("tr")

        transaction_tbody = transaction_tabs.find("tbody")
        transaction_rows = transaction_tbody.find_all("tr")

        currencies = {}
        for row in cash_rows[1:]:  # skip header row
            row_values = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(row_values) < 5:
                continue  # Skip incomplete rows

            currency_code = row_values[0].upper()
            cash_buying_rate = row_values[2]
            cash_selling_rate = row_values[3]

            currencies[currency_code] = {
                "currency_code": currency_code,
                "cash_buying_rate": cash_buying_rate,
                "cash_selling_rate": cash_selling_rate
            }

        for row in transaction_rows[1:]:  # skip header row
            row_values = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(row_values) < 5:
                continue  # Skip incomplete rows

            currency_code = row_values[0]
            transaction_buying_rate = row_values[2]
            transaction_selling_rate = row_values[3]

            if currency_code not in currencies:
                currencies[currency_code] = {
                    "currency_code": currency_code,
                    "cash_buying_rate": None,
                    "cash_selling_rate": None
                }
            currencies[currency_code].update({
                "transaction_buying_rate": transaction_buying_rate,
                "transaction_selling_rate": transaction_selling_rate
            })

            currencies[currency_code]["scrape_date"] = datetime.now().isoformat()
            currencies[currency_code]["rate_date"] = datetime.now().isoformat().split('T')[0]
            currencies[currency_code]["bank_code"] = "DASHEN"
        
        currency_values = []
        for currency_data in currencies.values():
            if len(currency_data) == 8:
                currency_values.append(currency_data)
        return currency_values
    except requests.RequestException as e:
        print(f"Error fetching data from Dashen Bank: {e}")
        return []
    
print(scrape_dashen_bank())
# Sample Output:
"""
{
    'bank_code': 'CBE',
    'currency_code': 'USD', 
    'currency_name': 'US Dollar', 
    'cash_buying_rate': '150.4809', 
    'cash_selling_rate': '153.4905', 
    'transaction_buying_rate': '150.4809', 
    'transaction_selling_rate': '153.4905', 
    'scrape_date': '2025-11-17T16:33:01.334862', 
    'rate_date': '2025-11-17'
}
"""