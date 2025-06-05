# 📚 Projekt áttekintés – TDKive

A **TDKive** egy webes archívum Tudományos Diákköri (TDK) dolgozatok számára, amely lehetővé teszi a kivonatok böngészését, keresését és statisztikai elemzését.  
A felhasználók egy keresőfelületen szűrhetik a kivonatokat év, szak, kulcsszavak, tanárok és diákok szerint.  
Az adminisztrátorok számára külön bejelentkezési lehetőség áll rendelkezésre, amely után új kivonatok tölthetők fel az adatbázisba.  
Az alkalmazás egy külön statisztikai oldalt is tartalmaz, ahol az összegyűlt adatok alapján vizuális statisztikák jelennek meg (pl. kulcsszófelhő, eloszlások, trendek).

---

## 🔍 Főbb funkciók

### ✅ Kivonatok keresése
- Kulcsszavas keresés a feltöltött TDK dolgozatok kivonatai között
- Szűrési lehetőségek: év, szak, cím, diák, tanár
- Találatok egy listában jelennek meg, minden dolgozat egy-egy külön elemként
- A keresési eredményekhez tartozik a teljes kivonat is

### 📊 Statisztikák megjelenítése
- Külön oldal a kivonatokból gyűjtött statisztikai adatokkal:
  - Dolgozatok számának éves megoszlása
  - Szakosztályok eloszlása
  - Legaktívabb tanárok
  - Leggyakoribb kulcsszavak (kulcsszófelhő)

### 🔐 Adminisztrátori feltöltőfelület
- Hitelesített admin felhasználó új kivonatokat tölthet fel JSON formátumban
- Automatikus normalizálás a tanárok nevére és indexelés Elasticsearch-ben

---

## 🛠 Technológiai háttér

### Backend
- **Nyelv**: Python
- **Keretrendszer**: FastAPI
- **Adatbázis**: Elasticsearch
- **Futtatás**: lokálisan
- Háttérfolyamat JSON generálás PDF fájlokból, tanárok nevének normalizálása
- Egyszerű bejelentkezés (admin / titok123)

### Frontend
- **Technológia**: React
- Önálló frontend, REST API-n keresztül kommunikál a backenddel
- 3 fő oldal:
  - Keresés
  - Feltöltés (admin)
  - Statisztikák

### Mesterséges intelligencia
- A kulcsszavak automatikus generálása egy nagy nyelvi modell segítségével történik (LLM)

### Adattárolás és infrastruktúra
- A PDF-ekből készült adatok JSON fájlokba kerülnek
- Feltöltés után Elasticsearch indexelés történik
- Nem használ Dockert, minden külön elindítva fut

---

## 🚀 Telepítés és futtatás – TDKive

Ez a rész segít a projekt lokális elindításában. A rendszer FastAPI backendből, React frontendből és Elasticsearchből áll.

### 🔧 Előfeltételek

Telepíteni szükséges:
- Python: `3.12.4`
- Node.js: `20.12.2`
- npm: `10.5.2`
- Elasticsearch: `8.16.0`

---

### 🖥️ Backend futtatása (FastAPI)

```bash
cd Backend/api
..\venv\Scripts\activate
uvicorn main:app --reload
```

📎 A backend elérhető: `http://localhost:8000`  
📦 Függőségek telepítése:  
```bash
pip install -r Backend/requirements.txt
```

---

### 🌐 Frontend futtatása (React)

```bash
cd frontend
npm install
npm start
```

📎 A frontend címe: `http://localhost:3000`  
🔗 Kommunikáció a backenddel: `http://localhost:8000`

---

### 🔍 Elasticsearch elindítása

```bash
cd elasticsearch-8.16.0\bin
elasticsearch.bat
```

📎 Elérhető itt: `http://localhost:9200`

---

### 📄 PDF → JSON konverzió

1. Helyezd el a PDF-eket:  
   `Backend/pdf_extractor_to_json/pdfs/`

2. Futtasd a konvertáló szkriptet:

```bash
cd Backend/pdf_extractor_to_json
python extract_text.py
```

3. Az eredmény JSON:  
   `Backend/pdf_extractor_to_json/output/all_projects.json`

---

### 📤 Adatok feltöltése (Admin felület)

- A frontend admin felületén `.json` fájl tölthető fel
- „Choose file” gomb → fájl kiválasztása → év megadása
- Backend automatikusan:
  - Indexeli az adatokat Elasticsearch-be
  - Normalizálja a tanárok neveit

#### Példa JSON formátumra:
```json
{
  "major": "Informatika",
  "year": 2015,
  "title": "Dolgozat címe",
  "students": [{
    "name": "Név",
    "major": "Sapientia EMTE, Informatika szak, 3. év"
  }],
  "teachers": [{
    "name": "Oktató",
    "university": "Sapientia EMTE"
  }],
  "content": "Dolgozatom célja ...",
  "keywords": ["kulcsszó1", "kulcsszó2"],
  "generated_keywords": ["kulcsszó3", "kulcsszó4"]
}
```

---

## 📁 Projektstruktúra

```
Allamvizsga/
├── .gitignore
├── README.md
│
├── Backend/
│   ├── requirements.txt
│   ├── venv/
│   ├── api/
│   │   ├── main.py
│   │   └── routes/
│   │       ├── search.py
│   │       ├── stats_routes.py
│   │       └── upload.py
│   ├── ElasticSearch/
│   │   ├── delete_by_year.py
│   │   ├── indexer.py
│   │   ├── normalize_teacher_names.py
│   │   ├── test.py
│   │   └── test2.py
│   └── pdf_extractor_to_json/
│       ├── extract_text.py
│       ├── process_all.py
│       ├── pdfs/
│       └── output/
│           └── all_projects.json
│
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── components/
│   │   │   ├── FilterPanel.js
│   │   │   ├── MajorsPerYearChart.js
│   │   │   ├── MostCommonKeywordsCloud.js
│   │   │   ├── PapersPerYearChart.js
│   │   │   ├── ResultList.js
│   │   │   ├── SearchBar.js
│   │   │   └── TopTeachersChart.js
│   │   ├── css/
│   │   │   ├── MajorsPerYearChart.css
│   │   │   ├── MostCommonKeywordsCloud.css
│   │   │   └── PapersPerYearChart.css
│   │   └── pages/
│   │       ├── SearchPage.js
│   │       ├── StatisticsPage.js
│   │       └── UploadPage.js
```
