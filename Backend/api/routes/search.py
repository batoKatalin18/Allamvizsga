from fastapi import APIRouter, Query
from elasticsearch import Elasticsearch

router = APIRouter()

# Hitelesített kapcsolat
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")
)

@router.get("/search")
def search(query: str = Query(..., min_length=1)):
    try:
        body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["title", "teachers.name"]
                }
            }
        }
        res = es.search(index="tdk_dolgozatok", body=body)
        hits = res["hits"]["hits"]
        return [hit["_source"] for hit in hits]
    except Exception as e:
        return {"detail": f"Hiba történt: {str(e)}"}
