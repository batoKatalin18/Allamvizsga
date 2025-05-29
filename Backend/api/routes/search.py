from fastapi import APIRouter, Query
from elasticsearch import Elasticsearch
from typing import Optional
from fastapi import Query

router = APIRouter()

# Hitelesített kapcsolat
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")
)

@router.get("/search")
def search(
    query: Optional[str] = Query(None),
    major: Optional[str] = Query(None),
    year: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    student: Optional[str] = Query(None),
    teacher: Optional[str] = Query(None)
):
    try:
        must_clauses = []

        if query:
            must_clauses.append({
                "multi_match": {
                    "query": query,
                    "fields": ["title", "content", "keywords", "generated_keywords"]
                }
            })

        if major:
            must_clauses.append({"term": {"major.keyword": major}})
        if year:
            must_clauses.append({"term": {"year": year}})
        if title:
            must_clauses.append({"match": {"title": title}})
        if student:
            must_clauses.append({"match": {"students.name": student}})
        if teacher:
            must_clauses.append({"match": {"teachers.name": teacher}})

        if not must_clauses:
            body = {"query": {"match_all": {}}}
        else:
            body = {
                "query": {
                    "bool": {
                        "must": must_clauses
                    }
                }
            }

        res = es.search(index="tdk_dolgozatok", body=body, size=1000)
        hits = res["hits"]["hits"]

        return [hit["_source"] for hit in hits]

    except Exception as e:
        return {"detail": f"Hiba történt: {str(e)}"}
    
@router.get("/filters")
def get_filters():
    try:
        aggs_body = {
            "size": 0,
            "aggs": {
                "years": {
                    "terms": {"field": "year", "size": 1000, "order": {"_key": "desc"}}
                },
                "majors": {
                    "terms": {"field": "major.keyword", "size": 1000}
                }
            }
        }

        res = es.search(index="tdk_dolgozatok", body=aggs_body)
        years = [bucket["key"] for bucket in res["aggregations"]["years"]["buckets"]]
        majors = [bucket["key"] for bucket in res["aggregations"]["majors"]["buckets"]]

        return {"years": years, "majors": majors}
    except Exception as e:
        return {"detail": f"Hiba a filterek lekérdezésekor: {str(e)}"}

