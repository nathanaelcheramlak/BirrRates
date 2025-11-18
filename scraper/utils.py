from pymongo.errors import BulkWriteError

def format_currency_code(code: str) -> str:
    """Format currency code to uppercase and strip whitespace."""
    return code.strip().upper()

def format_currency_name(name: str) -> str:
    """Format currency name to uppercase and strip whitespace."""
    return name.strip().upper()

def call_scraper(bank_code: str):
    from scraper.banks.cbe import scrape_cbe
    from scraper.banks.dashen_bank import scrape_dashen_bank

    if bank_code == "CBE":
        return scrape_cbe()
    elif bank_code == "DASHEN":
        return scrape_dashen_bank()
    else:
        raise ValueError(f"Unknown bank: {bank_code}")
    

def insert_rate_to_db(datas):
    if not datas:
        return None
    try:
        print('Inserting Rates to DB...')
        from api.config.database import mongodb
        collection = mongodb.get_collection('exchange_rates')

        if isinstance(datas, dict):
            datas = [datas]
        
        result = collection.insert_many(datas)
        print('Insertion Complete.', f"Inserted {len(result.inserted_ids)} documents")
        return result
        
    except BulkWriteError as e:
        print("Already scraped and inserted to database.")
    except Exception as e:
        print(f"Unexpected error during insertion: {e}")
        return None