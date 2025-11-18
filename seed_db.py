
from api.config.database import mongodb
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Load collections
bank_collection = mongodb.get_collection("banks")
currency_collection = mongodb.get_collection("currencies")
exchange_rate_collection = mongodb.get_collection("exchange_rates")

def create_indexes():
    print("Creating indexes...")
    bank_collection.create_index([("bank_code", 1)], unique=True)
    currency_collection.create_index([("currency_code", 1)], unique=True)
    exchange_rate_collection.create_index([("bank_code", 1), ("currency_code", 1), ("rate_date", 1)], unique=True)
    print("Indexes created.")

def seed_banks():
    try:
        print("Seeding banks collection...")
        banks = [
            {"name": "Commercial Bank of Ethiopia", "bank_code": "CBE", "scrape_url": os.getenv("DEFAULT_CBE_URL")},
            {"name": "Dashen Bank", "bank_code": "DASHEN", "scrape_url": os.getenv("DEFAULT_DASHEN_URL")}
        ]
        bank_collection.insert_many(banks)
        print("Seeded banks collection.")
    except Exception as e:
        print(f"Error seeding banks collection")

def seed_currencies():
    try:
        print("Seeding currencies collection...")
        currencies = [
            {"name": "ETHIOPIAN BIRR", "currency_code": "ETB"}, 
            {"name": "US DOLLAR", "currency_code": "USD"},
            {"name": "EURO", "currency_code": "EUR"},
            {"name": "POUND STERLING", "currency_code": "GBP"},
            {"name": "CANADIAN DOLLAR", "currency_code": "CAD"},
            {"name": "UNITED ARAB EMIRATES DIRHAM", "currency_code": "AED"},
            {"name": "SAUDI RIYAL", "currency_code": "SAR"},
            {"name": "CHINESE YUAN", "currency_code": "CNY"}
        ]
        currency_collection.insert_many(currencies)
        print("Seeded currencies collection.")
    except Exception as e:
        print(f"Error seeding currencies collection: {e}")

def clear_collection(collection_name: str):
    collection = mongodb.get_collection(collection_name)
    result = collection.delete_many({})
    print(f"Cleared {result.deleted_count} documents from {collection_name} collection.")

if __name__ == "__main__":
    create_indexes()    
    seed_banks()
    seed_currencies()
    