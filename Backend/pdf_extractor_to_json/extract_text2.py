import pdfplumber
import spacy
import pytextrank
import string
import random

nlp = spacy.load("xx_ent_wiki_sm")

if 'sentencizer' not in nlp.pipe_names:
    nlp.add_pipe('sentencizer')
if 'textrank' not in nlp.pipe_names:
    nlp.add_pipe('textrank')

# Egyszerű stopwords lista magyar és angol szavakkal
stopwords = set([
   'az', 'a', 'és', 'vagy', 'mint', 'is', 'hogy', 'de', 'mert', 'ha',
    'volt', 'van', 'lesz', 'egy', 'ez', 'ami', 'amiért', 'ehhez', 'ahhoz',
    'arra', 'ide', 'oda', 'itt', 'ott', 'ilyen', 'olyan', 'sőt', 'továbbá',
    'pedig', 'nem', 'úgy', 'ugyan', 'azt', 'azon', 'ezt', 'abból', 'amely',
    'akár', 'valamint', 'volna', 'lenne', 'még', 'ezen', 'fontos', 'ezért',
    'célom', 'így', 'ezzel', 'hogyan', 'ennek', 'módszerek', 'jelen',
    'dolgozatom', 'jelenleg', 'eredményeim', 'hanem', 'lehet', 'minden',
    'mindezek', 'ugyanakkor', 'célkitűzés', 'például', 'kutatásom',
    'következtetések', 'kutatásomban', 'választ', 'kutatási',
    'feltételezhető', 'napjainkban', 'ilyenkor', 'esetleg', 'napjaink',
    'rendelkezünk', 'klasszikus', 'legfőbb', 'azokra', 'melyet', 'azért',
    'biztosítja', 'ekkor', 'kell', 'azzal', 'megvizsgálom', 'nyújtott',
    'jól', 'először', 'miként', 'alapfeltevésem', 'simulinkben',
    'istván', 'általános', 'jelkódolás', 'pontosságának', 'vizsgálatomban',
    'kérdezek', 'vizuális', 'követnie', 'tudja', 'módon', 'nagyon',
    'mindhárom', 'megfelelően', 'kiegészítő', 'concluzia', 'mindemellett',
    'telefonon', 'erre', 'leírják', 'egyre', 'kell', 'fél', 'sajnos',
    'különösen', 'helyet', 'alkalmazott', 'másodlagos', 'mikor', 'meg',
    'kialakult', 'viszont', 'valamint', 'semmi', 'tapasztalati', 'léteznek',
    'elkezdeni', 'készítettünk', 'aktuális', 'ilyen', 'munkánk', 'rájöttek',
    'bizonyított', 'nagymértékű', 'feladatra', 'alkalmaz', 'alkalmazható',
    'amikor', 'tanulási', 'projektünk', 'időtartamon', 'ideális', 'kutatásaink',
    'arra', 'valószínűleg', 'mire', 'manapság', 'másfelől', 'gyakran',
    'elemek', 'járul', 'hozzá', 'két', 'Emellett'
])



def generate_keywords(text, num_keywords=5):
    doc = nlp(text)
    keywords = []

    for phrase in doc._.phrases:
        phrase_text = phrase.text.strip()

        # Szavak kisbetűsítve, írásjelek eltávolítva
        words = [w.strip(string.punctuation).lower() for w in phrase_text.split()]

        # Ha bármelyik szó szerepel a stopwords listában, ugorjuk
        if any(word in stopwords for word in words):
            continue

        # Ha túl hosszú kifejezés, opcionálisan elutasítjuk (itt: 3 szónál több)
        if len(words) > 3:
            continue

        keywords.append(phrase_text)

        if len(keywords) >= num_keywords:
            break

    return keywords



def extract_projects_from_pdf_v2(pdf_path, hardcoded_year=2025, hardcoded_major="Neveléstudomány"):
    projects = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_lines = []
            for page in pdf.pages:
                if page.extract_text():
                    text_lines.extend(page.extract_text().splitlines())

            i = 0
            while i < len(text_lines):
                # Keressük a dolgozat kezdő sorát (cím)
                title = text_lines[i].strip()

                # Alapellenőrzés, hogy legyen elég sor a struktúrához
                if i + 5 >= len(text_lines):
                    break

                students_line = text_lines[i + 1].strip()
                students_major = text_lines[i + 2].strip()
                mentor_label = text_lines[i + 3].strip()
                teachers_line = text_lines[i + 4].strip()
                teachers_university = text_lines[i + 5].strip()

                # Ellenőrizzük a "Témavezető:" vagy "Témavezetők:" sort
                if mentor_label not in ["Témavezető:", "Témavezetők:"]:
                    i += 1
                    continue

                students = [{"name": s.strip(), "major": students_major} for s in students_line.split(",") if s.strip()]
                teachers = [{"name": t.strip(), "university": teachers_university} for t in teachers_line.split(",") if t.strip()]

                # Content és kulcsszavak keresése i+6-tól
                content_lines = []
                keywords = []
                i_content = i + 6
                kulcsszavak_vege = False

                while i_content < len(text_lines):
                    line = text_lines[i_content].strip()

                    if line.startswith("Kulcsszavak:"):
                        after_colon = line[len("Kulcsszavak:"):].strip()
                        # Kulcsszavak utáni rész lehet üres is, vagy kulcsszavak vesszővel elválasztva
                        # Megnézzük, hogy van-e a végén pont
                        if after_colon.endswith("."):
                            kulcsszavak_vege = True
                            after_colon = after_colon[:-1].strip()  # levágjuk a pontot
                        else:
                            kulcsszavak_vege = False

                        # Ha van szöveg, bontjuk kulcsszavakra, ha nincs, akkor üres lista
                        if after_colon:
                            keywords = [kw.strip() for kw in after_colon.split(",") if kw.strip()]
                        else:
                            keywords = []

                        # Ha a pont már megvolt, dolgozat vége, kilépünk
                        if kulcsszavak_vege:
                            i_content += 1
                            break
                    else:
                        if not kulcsszavak_vege:
                            content_lines.append(line)
                        else:
                            # Ha már vége a kulcsszavaknak, nem kell tovább gyűjteni
                            break

                    i_content += 1

                content = " ".join(content_lines).strip()
                generated_keywords = generate_keywords(content)

                project = {
                    "major": hardcoded_major,
                    "year": hardcoded_year,
                    "title": title,
                    "students": students,
                    "teachers": teachers,
                    "content": content,
                    "keywords": keywords,
                    "generated_keywords": generated_keywords
                }

                projects.append(project)

                # Következő dolgozat kezdete a kulcsszavak végét követő sorból
                i = i_content

    except Exception as e:
        print(f"Hiba történt a PDF feldolgozása során ({pdf_path}): {e}")

    return projects


# Tesztelés
if __name__ == "__main__":
    pdf_path = "pdfs/uj_szerkezetu.pdf"
    projects = extract_projects_from_pdf_v2(pdf_path)
    from pprint import pprint
    pprint(projects)
