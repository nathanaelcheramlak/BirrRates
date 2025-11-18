import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from api.config.database import mongodb
from utils import call_scraper

def scrape_all():
    bank_collection = mongodb.get_collection('banks')
    banks_cursor = bank_collection.find({})
    banks = list(banks_cursor)
    print('Found banks:', banks)

    for bank in banks:
        bank_name = bank['name']
        bank_code = bank['bank_code']

        data = call_scraper(bank_code)
        if not data:
            print(f'No Data found for {bank_name}!')
            continue

        print(f'Scraped data for {bank_name}: {data}')
        from utils import insert_rate_to_db
        insert_rate_to_db(data)
    
if __name__ == "__main__":
    scrape_all()
            
        