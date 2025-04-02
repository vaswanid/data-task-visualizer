# === utils.py ===
import json
import csv
from datetime import datetime
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data"


def load_json_data():
    with open(DATA_PATH / "source_a.json") as f:
        data = json.load(f)
    print("✅ JSON data:", data)
    return data


def load_csv_data():
    with open("backend/data/source_b.csv") as f:    
        reader = csv.DictReader(f)
        data = list(reader)
    print("✅ CSV data:", data)
    return data

def clean_data(records):
    for r in records:
        r['price'] = float(r['price'])
        r['date_of_sale'] = datetime.strptime(r['date_of_sale'], "%Y-%m-%d").date()
        r['discount'] = float(r.get('discount', 0))
        r['warranty_years'] = int(r.get('warranty_years', 0))
        r['is_new'] = r.get('is_new', 'True') == 'True'
        r['mileage'] = float(r.get('mileage', 0))
    return records


def merge_sources(source_a, source_b):
    return source_a + source_b
