# process_all.py

import os
import json
from extract_text import extract_projects_from_pdf
from extract_text2 import extract_projects_from_pdf_v2

PDF_DIR = "pdfs"
OUTPUT_PATH = "output/all_projects.json"

def process_all_pdfs():
    all_projects = []

    for filename in os.listdir(PDF_DIR):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(PDF_DIR, filename)
            print(f"📄 Feldolgozás: {filename}")
            projects = extract_projects_from_pdf_v2(pdf_path)
            all_projects.extend(projects)

    print(f"\n✅ Összesen {len(all_projects)} dolgozat lett feldolgozva.")

    # JSON mentése
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_projects, f, indent=2, ensure_ascii=False)

    print(f"📁 Mentve ide: {OUTPUT_PATH}")

if __name__ == "__main__":
    process_all_pdfs()
