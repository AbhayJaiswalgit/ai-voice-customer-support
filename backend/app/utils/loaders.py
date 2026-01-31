import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"

def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_products():
    return load_json("product_catalog.json")

def load_orders():
    return load_json("order_database.json")

def load_faqs():
    return load_json("product_faqs.json")

def load_policies():
    return load_json("policies.json")
    # with open(DATA_DIR / "policies.txt", "r", encoding="utf-8") as f:
    #     return f.read()
