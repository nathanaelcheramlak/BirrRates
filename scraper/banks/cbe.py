import requests
from dotenv import load_dotenv
from datetime import datetime
import os

load_dotenv()
DEFAULT_ENDPOINT = os.getenv("DEFAULT_CBE_URL")
DEFAULT_DATE = datetime.now().strftime("%Y-%m-%d")

def scrape_cbe(cbe_endpoint=DEFAULT_ENDPOINT, date=DEFAULT_DATE):
    """
    Scrape the Central Bank of Ethiopia (CBE) exchange rates.
    """
    if date:
        cbe_endpoint += f"&Date={date}"

    try:
        response = requests.get(cbe_endpoint)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data from CBE: {response.status_code}")
        currency_data = response.json()
        if not currency_data:
            raise Exception("No data found in CBE response")
        
        currencies = []
        currency_data_date = currency_data[0].get("Date")
        for exchange_rate in currency_data[0].get("ExchangeRate", []):
            # Extracting relevant fields
            cash_buy_rate = exchange_rate.get("cashBuying")
            cash_sell_rate = exchange_rate.get("cashSelling")
            transfer_buy_rate = exchange_rate.get("transactionalBuying")
            transfer_sell_rate = exchange_rate.get("transactionalSelling")

            currency_code = exchange_rate.get("currency", {}).get("CurrencyCode", "").upper()
            currency_name = exchange_rate.get("currency", {}).get("CurrencyName", "").upper()

            if not all([currency_code, currency_name, cash_buy_rate, cash_sell_rate]):
                continue  # Skip incomplete data

            currencies.append({
                "bank_code": "CBE",
                "currency_code": currency_code,
                "currency_name": currency_name,
                "cash_buying_rate": cash_buy_rate,
                "cash_selling_rate": cash_sell_rate,
                "transaction_buying_rate": transfer_buy_rate,
                "transaction_selling_rate": transfer_sell_rate,
                "rate_date": currency_data_date,
                "scrape_date": datetime.now().isoformat()
            })

        return currencies
            
    except requests.RequestException as e:
        print(f"Error fetching data from CBE: {e}")
        return []


print(scrape_cbe(date="2025-11-15"))
# Sample Output:
"""
{
    'currency_code': 'USD', 
    'currency_name': 'US DOLLAR', 
    'cash_buying_rate': 150.5286, 
    'cash_selling_rate': 153.5392, 
    'transaction_buying_rate': 150.5286, 
    'transaction_selling_rate': 153.5392, 
    'rate_date': '2025-11-15', 
    'scrape_date': '2025-11-17T16:31:16.166901'
}
"""