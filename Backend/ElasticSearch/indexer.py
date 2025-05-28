from elasticsearch import Elasticsearch
import json

# 1. Csatlakozás Elasticsearch-hez jelszóval
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")  # használjuk az új jelszót
)

# 2. Index neve
INDEX_NAME = "tdk_dolgozatok"

# 3. Index létrehozása (mapping nélkül, alapértelmezetten)
if not es.indices.exists(index=INDEX_NAME):
    es.indices.create(index=INDEX_NAME)
    print(f"Index '{INDEX_NAME}' létrehozva.")

# 4. JSON betöltése
with open("pdf_extractor_to_json/output/all_projects.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 5. Dokumentumok indexelése
for i, doc in enumerate(data):
    res = es.index(index=INDEX_NAME, id=i+1, document=doc)
    print(f"Feltöltve: {res['result']} (ID: {i+1})")
