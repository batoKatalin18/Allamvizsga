import re
import pdfplumber
import spacy
import pytextrank

# NLP setup
nlp = spacy.load("xx_ent_wiki_sm")

if 'sentencizer' not in nlp.pipe_names:
    nlp.add_pipe('sentencizer')
if 'textrank' not in nlp.pipe_names:
    nlp.add_pipe('textrank')

def generate_keywords(text, num_keywords=5):
    doc = nlp(text)
    return [phrase.text for phrase in doc._.phrases[:num_keywords]]

def extract_major(text):
    return text.strip().replace("kivonatai", "").strip()

def extract_projects_from_pdf(pdf_path, hardcoded_year=2014):
    projects = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text_lines = page.extract_text().splitlines()
                words = page.extract_words(use_text_flow=True, keep_blank_chars=False, extra_attrs=["size", "fontname"])

                if not text_lines:
                    continue

                major = extract_major(text_lines[0])
                year = hardcoded_year

                i = 0
                current_project = {}
                while i < len(text_lines):
                    line = text_lines[i].strip()

                    # --- Title detection ---
                    if line and not any(tag in line for tag in ["Szerző(k):", "Irányító tanár(ok):", "Kivonat:", "Kulcsszavak:"]):
                        title_lines = [line]
                        i += 1
                        while i < len(text_lines) and not text_lines[i].strip().startswith("Szerző(k):"):
                            if text_lines[i].strip():
                                title_lines.append(text_lines[i].strip())
                            i += 1
                        current_project = {
                            "major": major,
                            "year": year,
                            "title": " ".join(title_lines),
                            "students": [],
                            "teachers": [],
                            "content": "",
                            "keywords": [],
                            "generated_keywords": []
                        }
                        continue

                    # --- Szerző(k) ---
                    if "Szerző(k):" in line:
                        author_lines = []
                        i += 1
                        while i < len(text_lines):
                            l = text_lines[i].strip()
                            if not l or "Irányító tanár(ok):" in l:
                                break
                            author_lines.append(l)
                            i += 1

                        author_block = " ".join(author_lines)
                        matches = re.findall(r'([^()]+?)\s*\(([^()]+?)\)', author_block)

                        for name, raw_major in matches:
                            current_project["students"].append({
                                "name": name.strip(),
                                "major": raw_major.strip()
                            })
                        continue

                    # --- Irányító tanár(ok) ---
                    if "Irányító tanár(ok):" in line:
                        i += 1
                        while i < len(text_lines):
                            l = text_lines[i].strip()
                            if not l or "Kivonat:" in l:
                                break
                            name = re.sub(r'\s*\(.*?\)', '', l).strip()
                            if name:
                                current_project["teachers"].append({
                                    "name": name,
                                    "university": ""
                                })
                            i += 1
                        continue

                    # --- Kivonat ---
                    if "Kivonat:" in line:
                        content_paragraph = []
                        i += 1
                        while i < len(text_lines):
                            l = text_lines[i].strip()
                            if not l or "Kulcsszavak:" in l:
                                break
                            content_paragraph.append(l)
                            i += 1
                        current_project["content"] = " ".join(content_paragraph).strip()
                        current_project["generated_keywords"] = generate_keywords(current_project["content"])
                        continue

                    # --- Kulcsszavak: pontos hozzárendeléshez szöveg alapján keresünk indexet ---
                    if "Kulcsszavak:" in line:
                        keyword_words = []
                        kulcsszo_word_index = None

                        for idx, w in enumerate(words):
                            if w["text"].startswith("Kulcsszavak"):
                                kulcsszo_word_index = idx
                                break

                        if kulcsszo_word_index is not None:
                            for w in words[kulcsszo_word_index + 1:]:
                                if "Italic" not in w["fontname"]:
                                    break
                                keyword_words.append(w["text"])

                        keyword_block = " ".join(keyword_words)
                        current_project["keywords"] = [kw.strip() for kw in keyword_block.split(",") if kw.strip()]
                        projects.append(current_project)
                        current_project = {}
                        i += 1
                        continue




                    i += 1

    except Exception as e:
        print(f"Hiba történt a PDF feldolgozása során ({pdf_path}): {e}")

    return projects

# Teszt
if __name__ == "__main__":
    test_path = "pdfs/kozeg.pdf"
    result = extract_projects_from_pdf(test_path)
    from pprint import pprint
    pprint(result)
