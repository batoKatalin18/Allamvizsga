from elasticsearch import Elasticsearch

# Csatlakozás az Elasticsearch-hez
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")  # saját jelszavad
)

# Index neve
INDEX_NAME = "tdk_dolgozatok"

# Törlendő év
year_to_delete = "2024"

# Ellenőrzés: van-e ilyen dokumentum
search_result = es.count(index=INDEX_NAME, body={
    "query": {
        "term": {
            "year": year_to_delete
        }
    }
})

print(f"📄 {search_result['count']} dokumentum található a(z) {year_to_delete} évhez.")

if search_result['count'] == 0:
    print("Nincs mit törölni.")
else:
    # Dokumentumok törlése a year mező alapján
    delete_result = es.delete_by_query(index=INDEX_NAME, body={
        "query": {
            "term": {
                "year": year_to_delete
            }
        }
    })

    print(f"🗑️ Törölve: {delete_result['deleted']} dokumentum a(z) {year_to_delete} évből.")
