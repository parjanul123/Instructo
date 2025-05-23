import time
import os
import json
from duckduckgo_search import DDGS

CACHE_FILE = "resurse/cautare_cache.json"

# === Încarcă cache-ul dacă există ===
def incarca_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

# === Salvează cache-ul ===
def salveaza_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

# === Cache local pentru căutare ===
cache = incarca_cache()

# === Funcție căutare pe internet cu cache și delay ===
def cauta_pe_internet(subiect):
    # Verifică în cache
    if subiect in cache:
        return cache[subiect]

    # Adaugă delay pentru a evita blocarea
    time.sleep(3)

    # Încercare de căutare cu DuckDuckGo
    rezultate = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(subiect, region="ro-ro", safesearch="Moderate", max_results=3):
                rezultate.append(r['body'])
    except Exception as e:
        return f"⚠️ Eroare la căutarea pe internet: {str(e)}"

    # Dacă am rezultate, le salvez în cache
    rezultate_text = "\n".join(rezultate) if rezultate else "⚠️ Nu am găsit rezultate."
    cache[subiect] = rezultate_text
    salveaza_cache(cache)
    return rezultate_text
