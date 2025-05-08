from duckduckgo_search import DDGS

def cauta_pe_internet(subiect):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(subiect, region="ro-ro", safesearch="Moderate", max_results=3):
            results.append(r['body'])
    return "\n".join(results) if results else "Nu am găsit informații suplimentare online."
