from elasticsearch import Elasticsearch, helpers
import re

# Elasticsearch kapcsolódás
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")  # használjuk az új jelszót
)

INDEX_NAME = "tdk_dolgozatok"  # vagy ami nálad van

def normalize_name(name):
    name = name.lower()
    name = re.sub(r'\b(dr|prof)\.?\b', '', name)  # előtagok
    name = re.sub(r'\begyetemi\b', '', name)
    name = re.sub(r'\b(tanár|adjunktus|docens)\b', '', name)
    name = re.sub(r'[^\w\s]', '', name)  # pontok, vesszők stb. eltávolítása
    name = re.sub(r'\s+', ' ', name).strip()
    name = name.title()  # nagy kezdőbetű minden szóban
    return name


# Lekérjük az összes dokumentumot (max 10k-ig simán)
def fetch_all_docs():
    return helpers.scan(es, index=INDEX_NAME, query={"query": {"match_all": {}}})

# Frissítési művelet: új mező hozzáadása
def update_docs_with_normalized_names():
    actions = []
    for doc in fetch_all_docs():
        doc_id = doc['_id']
        source = doc['_source']
        if 'teachers' in source:
            normalized_teachers = []
            for t in source['teachers']:
                name = t.get('name', '')
                norm_name = normalize_name(name)
                t['normalized_name'] = norm_name
                normalized_teachers.append(t)

            action = {
                "_op_type": "update",
                "_index": INDEX_NAME,
                "_id": doc_id,
                "doc": {
                    "teachers": normalized_teachers
                }
            }
            actions.append(action)

    helpers.bulk(es, actions)
    print(f"{len(actions)} dokumentum frissítve.")

# Futtatás
if __name__ == "__main__":
    update_docs_with_normalized_names()
