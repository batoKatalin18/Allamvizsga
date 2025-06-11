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

# Magyar stopword lista 
STOP_WORDS = {
    'az', 'a', 'és', 'vagy', 'mint', 'is', 'hogy', 'de', 'mert', 'ha',
    'volt', 'van', 'lesz', 'egy', 'ez', 'ami', 'amiért', 'ehhez', 'ahhoz',
    'arra', 'ide', 'oda', 'itt', 'ott', 'ilyen', 'olyan', 'sőt', 'továbbá',
    'pedig', 'nem', 'úgy', 'ugyan', 'azt', 'azon', 'ezt', 'abból', 'arra',
    'amely', 'akár', 'valamint', 'volna', 'lenne', 'még', 'ezen', 'fontos', 
    'ezért', 'célom', 'így', 'ezzel', 'hogyan', 'ennek', 'ktatásom', 'módszerek', 
    'jelen', 'dolgozatom', 'jelenleg', 'eredményeim', 'hanem', 'lehet', 'minden', 
    'mindezek', 'ugyanakkor', 'célkitűzés', 'például', 'kutatásom' ,
    'következtetések' , 'kutatásomban' , 'választ' , 'kutatási' , 'feltételezhető' , 
    'napjainkban' , 'meine' , 'ilyenkor', 'esetleg', 'napjaink', 'rendelkezünk',
    'jó stratégiának', 'alapján vissza', 'elemezése mellett', 'klasszikus', 'lehet alkalmazni', 
    'módszert összehasonlítsa sebesség', 'hanem akár', 'helyett az', 'alapján megállapítottuk', 
    'dobó-nagy', 'legfőbb', 'azokra', 'melyet', 'azért', 'biztosítja', 'ekkor', 'kell létrehozni', 
    'megtervezett fogaskerékhajtáson', 'dolgozatunkban', 'azokra', 'csiszolásokat kell', 
    'javították ki', 'legyen legyőzni', 'köszörüléssel', 'javítani', 'így akár személyi számítógépről', 
    'kell legyen ahhoz' , 'felmerülő konfliktushelyzetekre', 'alakulnak ki', 'olyan hatást' , 
    'bemutatásra kerül', 'levő kockák', 'fél tonnát', 'nélküli kapcsolaton' , 
    'lefordított hanganyagot kell eljuttassa', 'rendezett adatok között kutatok', 
    'eldöntésén alapszik', 'határozza meg' , 'nagy terhelhetőség mellett', 'mindez', 
    '4. év) irányító tanár(ok): dr. máté márton (sapientia emte', 'kell' , 'azzal', 
    'megvizsgálom', 'nyújtott' , 'jól', 'jó munkák körébe' , 'említett problémák', 
    'először', 'egy jelet' , 'azok kontrollálhatatlan', 'miként befolyásolják', 
    'alapfeltevésem' , 'olyan hajtóművet készíthetünk', 'simulinkben', 'istván általános' , 
    'jelkódolás pontosságának', 'olyan módszerek kifejlesztésére', 'vizsgálatomban', 
    'kérdezek rá' , 'vizuális képet add', 'követnie kell', 'egy lokális', 'dolgozatunk' , 
    'tudja követni', 'módon továbbítja', 'jelszó mellett', 'nagyon' , 'mindhárom', 
    'módszerek mellett', 'megfelelően helytáll', 'egy autónk' , 'mellett megoldottam', 
    'egy globális', 'kiegészítő', '3d-s grafikának hiszünk' , 'eszközzel végzett', 
    'concluzia', 'mindemellett' , 'telefonon', 'elhelyezkedő turistalátványosságokat', 
    'alkalmazni feldolgozási folyamatokban', 'erre', 'leírják', 'előállított betétkések', 
    'egyre', 'studiul', 'ezekbe', 'kell követnie', 'nyújtson', 'fél', 'jó hatásfok', 
    'sajnos', 'különösen', 'grafikai megoldásokon', 'helyet kapni', 'alkalmazott', 
    'hogy henger', 'másodlagos', 'mikor', 'meg', 'kialakult', 'arra keresem', 'viszont', 
    'járműipar minden', 'emberek lennénk', 'valamint grafikusan', 'szerszámba', 'meg az erő', 
    'elektrosztatikus teret', 'pozicionálás feladatán', 'autót', 'meg az', 'eleget kell', 
    'megtalálhatók', 'emberek számára', 'semmi', 'tapasztalati', 'legyen kiszámítani', 
    'léteznek', 'elkezdeni', 'készítettünk', 'aktuális', 'az apache cassandra', 
    'ilyen módon', 'munkánk', 'rájöttek', 'kell tálalnunk', 'bizonyított', 
    'hány rögzített pontú', 'nagymértékű', 'feladatra hivatottak', 
    'alkalmaz rendszer kialakítása', 'egy hőszivattyú', 'hőenergia szállításáért', 
    'ilyen módon meglévő', 'amellyel gyorsan', 'meg lehet', 'amikor', 'tanulási', 'egy webalapú', 
    'alkalmazhatóak az autóiparban', 'megértését könnyebbé tegye', 'projektünk', 
    'jó hatással lehet', 'mérésére van szükség', 'időtartamon belül', 'kell darabolni', 'ideális', 
    'hőmérsékletű hőforrásokat', 'épített bináris', 'kutatásaink', 'arra hívatott', 
    'felvételek előszűrését', 'alapján történő szegmentálására', 'köszönhetően ötvözni', 
    'nélküli útválasztó', 'hanem alternatív megközelítésekben', 'valószínűleg', 'egy hőszivattyú-berendezéssel', 
    'mire', 'hangon kell hozzá', 'kell odafigyelnünk', 'rubik-kockáról mind logikai', 'akkor sikerül csökkentenünk', 
    'manapság', 'tudja', 'másfelől', 'gyakran', 'elemek mellett', 'járul hozzá', 'két', 'meine', 'meine'
}

@router.get("/api/most-common-keywords")
def get_most_common_keywords(
    year: str = Query(...),
    major: str = Query("all")
):
    must_clauses = []

    if year != "all":
        must_clauses.append({"term": {"year": int(year)}})
    if major != "all":
        must_clauses.append({"term": {"major.keyword": major}})

    body = {
        "size": 10000,
        "_source": ["keywords", "generated_keywords"],
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

    res = es.search(index=INDEX_NAME, body=body)
    keyword_counter = {}

    for hit in res["hits"]["hits"]:
        all_keywords = []
        # Egyesítjük a két lista tartalmát, ha léteznek
        all_keywords.extend(hit["_source"].get("keywords", []))
        all_keywords.extend(hit["_source"].get("generated_keywords", []))

        for kw in all_keywords:
            kw = kw.lower()
            if kw not in STOP_WORDS and len(kw) > 2:
                keyword_counter[kw] = keyword_counter.get(kw, 0) + 1

    sorted_keywords = sorted(keyword_counter.items(), key=lambda x: -x[1])[:100]

    return [{"text": k, "value": v} for k, v in sorted_keywords]







