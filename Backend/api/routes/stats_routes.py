from fastapi import APIRouter, Query
from elasticsearch import Elasticsearch

router = APIRouter()

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")
)

INDEX_NAME = "tdk_dolgozatok"

@router.get("/api/papers-per-year")
def get_papers_per_year():
    response = es.search(
        index=INDEX_NAME,
        body={
            "size": 0,
            "aggs": {
                "papers_per_year": {
                    "histogram": {
                        "field": "year",
                        "interval": 1,           # évente csoportosítva
                        "min_doc_count": 1
                    }
                }
            }
        }
    )

    result = [
        {"year": int(bucket["key"]), "count": bucket["doc_count"]}
        for bucket in response["aggregations"]["papers_per_year"]["buckets"]
    ]

    return result

@router.get("/api/available-years")
def get_available_years():
    response = es.search(
        index=INDEX_NAME,
        size=0,
        aggs={
            "years": {
                "terms": {
                    "field": "year",
                    "size": 100,
                    "order": { "_key": "asc" }
                }
            }
        }
    )
    years = [bucket["key"] for bucket in response["aggregations"]["years"]["buckets"]]
    return years


@router.get("/api/majors-by-year")
def get_majors_by_year(year: int = Query(...)):
    response = es.search(
        index=INDEX_NAME,
        size=0,
        query={"term": {"year": year}},
        aggs={
            "majors": {
                "terms": {
                    "field": "major.keyword",  # .keyword for exact match
                    "size": 100
                }
            }
        }
    )
    return [
        {"name": bucket["key"], "value": bucket["doc_count"]}
        for bucket in response["aggregations"]["majors"]["buckets"]
    ]

@router.get("/api/top-teachers")
def get_top_teachers(
    year: str = Query(...),
    major: str = Query("all")
):
    must_clauses = []

    if year != "all":
        must_clauses.append({"term": {"year": int(year)}})
    if major != "all":
        must_clauses.append({"term": {"major.keyword": major}})

    body = {
        "size": 0,
        "query": {
            "bool": {
                "must": must_clauses
            }
        },
        "aggs": {
            "top_teachers": {
                "terms": {
                    "field": "teachers.normalized_name.keyword",  # multivalued keyword mező
                    "size": 10
                }
            }
        }
    }

    res = es.search(index=INDEX_NAME, body=body)
    buckets = res["aggregations"]["top_teachers"]["buckets"]
    data = [{"name": bucket["key"], "count": bucket["doc_count"]} for bucket in buckets]
    return data






