from elasticsearch import Elasticsearch

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")
)

version = es.info()['version']['number']
print(f"Elasticsearch version: {version}")
