import os
import json
import datetime
from pathlib import Path
from pdf_utils import extract_headings, extract_relevant_paragraphs

def process_collection(collection_path: Path):
    input_json_path = collection_path / "challenge1b_input.json"
    output_json_path = collection_path / "challenge1b_output.json"
    pdf_dir = collection_path / "PDFs"

    with open(input_json_path, "r", encoding="utf-8") as f:
        input_data = json.load(f)

    persona = input_data["persona"]["role"]
    task = input_data["job_to_be_done"]["task"]
    challenge_id = input_data["challenge_info"]["challenge_id"]
    documents = input_data["documents"]

    extracted_sections = []
    subsection_analysis = []

    for idx, doc in enumerate(documents):
        filename = doc["filename"]
        title = doc["title"]
        pdf_path = pdf_dir / filename

        if not pdf_path.exists():
            print(f"⚠️ Skipping missing file: {filename}")
            continue

        # Section Titles
        sections = extract_headings(pdf_path, persona, task)
        for sec in sections:
            sec["document"] = filename
            extracted_sections.append(sec)

        # Subsections (Refined)
        refined = extract_relevant_paragraphs(pdf_path, persona, task)
        for para in refined:
            para["document"] = filename
            subsection_analysis.append(para)

    output_json = {
        "metadata": {
            "input_documents": [doc["filename"] for doc in documents],
            "persona": persona,
            "job_to_be_done": task,
            "processing_timestamp": datetime.datetime.now().isoformat(),
            "challenge_id": challenge_id
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(output_json, f, indent=2)

    print(f"✅ Done: {collection_path.name}")


def main():
    base_dir = Path(__file__).parent.parent
    for folder in base_dir.glob("Collection*"):
        if folder.is_dir():
            process_collection(folder)

if __name__ == "__main__":
    main()
