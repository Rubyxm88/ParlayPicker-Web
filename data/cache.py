# data/cache.py

import os
import json
from datetime import datetime, timedelta
from data.update_db import update_all

CACHE_FILE = "cache_status.json"
CACHE_TIMEOUT_MINUTES = 60

def read_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r") as f:
        return json.load(f)

def write_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump({"last_updated": datetime.utcnow().isoformat()}, f)

def is_cache_stale():
    cache = read_cache()
    last_str = cache.get("last_updated")
    if not last_str:
        return True
    last_time = datetime.fromisoformat(last_str)
    return datetime.utcnow() - last_time > timedelta(minutes=CACHE_TIMEOUT_MINUTES)

def run_cache_check():
    if is_cache_stale():
        print("🔁 Cache stale — refreshing data.")
        update_all()
        write_cache()
    else:
        print("✅ Cache is fresh. No update needed.")

def get_last_updated():
    cache = read_cache()
    ts = cache.get("last_updated")
    return datetime.fromisoformat(ts) if ts else None

def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)
