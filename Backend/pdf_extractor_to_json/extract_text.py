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
    text = text.replace("szakosztály", "")
    text = text.replace("kivonatai", "")
    return text.strip()


def extract_projects_from_pdf(pdf_path, hardcoded_year=2015):
    projects = []

    try:
        with pdfplumber.open(pdf_path) as pdf:
            text_lines = []
            words = []
            for page in pdf.pages:
                if page.extract_text():
                    text_lines.extend(page.extract_text().splitlines())
                words.extend(page.extract_words(use_text_flow=True, keep_blank_chars=False, extra_attrs=["size", "fontname", "top"]))

            if not text_lines:
                return []

            major = extract_major(text_lines[0])
            year = hardcoded_year

            i = 0
            current_project = None
            while i < len(text_lines):
                line = text_lines[i].strip()

                # --- Új projekt kezdete ---
                if "Szerző(k):" in line:
                    # --- Cím visszakeresése ---
                    title_lines = []
                    j = i - 1
                    while j >= 0:
                        prev_line = text_lines[j].strip()
                        if not prev_line or any(tag in prev_line for tag in ["Kulcsszavak:", "Kivonat:", "Irányító tanár(ok):"]):
                            break
                        title_lines.insert(0, prev_line)
                        j -= 1

                    title_full = " ".join(title_lines)

                    # --- Major + "kivonatai" eltávolítása a cím elejéről ---
                    prefix_to_remove = f"{major} szakosztály kivonatai"
                    if title_full.startswith(prefix_to_remove):
                        title_full = title_full[len(prefix_to_remove):].strip(" :–-")

                    current_project = {
                        "major": major,
                        "year": year,
                        "title": title_full,
                        "students": [],
                        "teachers": [],
                        "content": "",
                        "keywords": [],
                        "generated_keywords": []
                    }

                    # --- Szerzők ---
                    i += 1
                    author_lines = []
                    while i < len(text_lines):
                        l = text_lines[i].strip()
                        if not l or "Irányító tanár(ok):" in l:
                            break
                        author_lines.append(l)
                        i += 1

                    author_block = " ".join(author_lines)
                    matches = re.findall(r'([^()]+?)\s*\(([^()]+?)\)', author_block)
                    if matches:
                        for name, raw_major in matches:
                            current_project["students"].append({
                                "name": name.strip(),
                                "major": raw_major.strip()
                            })
                    else:
                        for name_line in author_lines:
                            name = re.sub(r'\s*\(.*?\)', '', name_line).strip()
                            if name:
                                current_project["students"].append({
                                    "name": name,
                                    "major": ""
                                })

                # --- Irányító tanár(ok) blokk ---
                line = text_lines[i].strip()
                if current_project and line.startswith("Irányító tanár(ok):"):
                    i += 1
                    teacher_lines = []
                    while i < len(text_lines):
                        l = text_lines[i].strip()
                        if not l or "Kivonat:" in l or "Szerző(k):" in l:
                            break
                        teacher_lines.append(l)
                        i += 1

                    teacher_block = " ".join(teacher_lines)
                    matches = re.findall(r'([^()]+?)\s*\(([^()]+?)\)', teacher_block)
                    if matches:
                        for name, university in matches:
                            current_project["teachers"].append({
                                "name": name.strip(),
                                "university": university.strip()
                            })
                    else:
                        for name_line in teacher_lines:
                            name = re.sub(r'\s*\(.*?\)', '', name_line).strip()
                            if name:
                                current_project["teachers"].append({
                                    "name": name,
                                    "university": ""
                                })
                    continue

                # --- Kivonat ---
                if current_project and line.startswith("Kivonat:"):
                    i += 1
                    content_paragraph = []
                    while i < len(text_lines):
                        l = text_lines[i].strip()
                        if not l:
                            i += 1
                            continue
                        if "Kulcsszavak:" in l or "Szerző(k):" in l:
                            break
                        content_paragraph.append(l)
                        i += 1
                    current_project["content"] = " ".join(content_paragraph).strip()
                    current_project["generated_keywords"] = generate_keywords(current_project["content"])
                    continue

                # --- Kulcsszavak blokk (csak ha van aktuális projekt) ---
                # --- Kulcsszavak blokk (csak ha van aktuális projekt) ---
                if current_project and line.startswith("Kulcsszavak:"):
                    after_colon = line.split(":", 1)[1].strip()
                    if not after_colon:
                        i += 1
                        projects.append(current_project)
                        current_project = None
                        continue

                    italic_keywords = []
                    # Nézzük meg az első sort külön, hátha vannak benne dőlt szavak
                    line_words = [w for w in words if w["text"] in line]
                    italic_line_words = [w for w in line_words if "Italic" in w["fontname"] or "Oblique" in w["fontname"]]
                    italic_keywords.extend([w["text"] for w in italic_line_words])

                    i += 1
                    while i < len(text_lines):
                        next_line = text_lines[i].strip()
                        if not next_line:
                            i += 1
                            continue
                        line_words = [w for w in words if w["text"] in next_line]
                        italic_line_words = [w for w in line_words if "Italic" in w["fontname"] or "Oblique" in w["fontname"]]
                        if not italic_line_words:
                            break
                        italic_keywords.extend([w["text"] for w in italic_line_words])
                        i += 1

                    # kulcsszavak vesszővel vannak elválasztva, lehet, hogy egy-egy szó volt külön dőlt betűs szóként
                    joined = " ".join(italic_keywords)
                    current_project["keywords"] = [kw.strip() for kw in joined.split(",") if kw.strip()]
                    projects.append(current_project)
                    current_project = None
                    continue

                i += 1

            if current_project:
                projects.append(current_project)

    except Exception as e:
        print(f"Hiba történt a PDF feldolgozása során ({pdf_path}): {e}")

    return projects


# Teszt
if __name__ == "__main__":
    test_path = "pdfs/fordito.pdf"
    result = extract_projects_from_pdf(test_path)
    from pprint import pprint
    pprint(result)

#doltbetus kell legyen a teljes kulcszavas lista