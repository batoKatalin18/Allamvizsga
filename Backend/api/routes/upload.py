from fastapi import APIRouter, UploadFile, Form
from elasticsearch import Elasticsearch
import json
import logging
import re

router = APIRouter()

es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "fx7WSUS8vPcSS4KhXjyg")
)

# Logger konfigurálása
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Név normalizáló függvény
def normalize_name(name):
    name = name.lower()
    name = re.sub(r'\bdr\.?\b', '', name)
    name = re.sub(r'\bprof\.?\b', '', name)
    name = re.sub(r'\begyetemi\b', '', name)
    name = re.sub(r'\b(tanár|adjunktus|docens)\b', '', name)
    name = re.sub(r'\.', '', name)  # pont eltávolítása
    name = re.sub(r'\s+', ' ', name).strip()
    return name.title()  # visszakisbetű nagybetűs kezdőbetűkkel

@router.post("/upload")
async def upload_json(file: UploadFile, year: str = Form(...)):
    logger.info(f"Feltöltés indult: fájl={file.filename}, év={year}")
    try:
        contents = await file.read()
        logger.info("Fájl beolvasva, JSON parse kezdődik...")
        data = json.loads(contents)
        logger.info(f"{len(data) if isinstance(data, list) else 'N/A'} elem beolvasva a fájlból.")

        if not data or not isinstance(data, list):
            return {"detail": "A feltöltött fájl üres vagy nem megfelelő formátumú (pl. nem lista)."}

        res = es.search(
            index="tdk_dolgozatok",
            body={"query": {"term": {"year": year}}},
            size=1
        )
        if res["hits"]["total"]["value"] > 0:
            return {"detail": f"A(z) {year} év már szerepel, új feltöltés nem történt."}

        required_fields = {"major", "title", "students", "teachers", "content", "keywords", "generated_keywords"}

        for i, doc in enumerate(data):
            if not isinstance(doc, dict):
                return {"detail": f"A(z) {i+1}. elem nem objektum (dict)."}

            missing = required_fields - doc.keys()
            if missing:
                return {"detail": f"A(z) {i+1}. dokumentumból hiányzó mezők: {', '.join(missing)}."}

            if not isinstance(doc["students"], list) or not all("name" in s and "major" in s for s in doc["students"]):
                return {"detail": f"A(z) {i+1}. dokumentum 'students' mezője hibás vagy hiányos."}

            if not isinstance(doc["teachers"], list) or not all("name" in t and "university" in t for t in doc["teachers"]):
                return {"detail": f"A(z) {i+1}. dokumentum 'teachers' mezője hibás vagy hiányos."}

        logger.info(f"{len(data)} dokumentum indexelése indul...")

        for doc in data:
            doc["year"] = int(year)
            for teacher in doc["teachers"]:
                teacher["normalized_name"] = normalize_name(teacher["name"])
            es.index(index="tdk_dolgozatok", document=doc)

        logger.info(f"Sikeres feltöltés: {len(data)} dokumentum indexelve.")
        return {"message": f"Sikeresen feltöltöttél {len(data)} dokumentumot a(z) {year}. évhez."}

    except Exception as e:
        logger.exception("Hiba történt a feltöltés során:")
        return {"detail": f"Hiba a feldolgozás során: {str(e)}"}

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "titok123"

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"success": True}
    return {"success": False, "detail": "Hibás felhasználónév vagy jelszó."}