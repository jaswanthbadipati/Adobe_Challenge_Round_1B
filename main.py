
import os
import json
from pathlib import Path
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_persona_task(path):
    with open(path, 'r') as f:
        return json.load(f)

def get_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    sections = []
    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text.split()) > 5:
                sections.append({
                    "pdf": os.path.basename(pdf_path),
                    "page": page_num,
                    "text": text
                })
    return sections

def rank_sections(sections, query, top_k=5):
    texts = [s["text"] for s in sections]
    embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)

    hits = util.semantic_search(query_embedding, embeddings, top_k=top_k)[0]
    ranked = []
    for hit in hits:
        section = sections[hit['corpus_id']]
        section["score"] = float(hit['score'])
        ranked.append(section)
    return ranked

def summarize_text(text):
    return text[:500] + "..." if len(text) > 500 else text

def process(input_dir, persona_task_path, output_path):
    task_data = load_persona_task(persona_task_path)
    persona, task = task_data["persona"], task_data["task"]
    query = f"{persona}: {task}"

    all_sections = []
    for pdf in Path(input_dir).glob("*.pdf"):
        all_sections.extend(get_pdf_text(pdf))

    top_sections = rank_sections(all_sections, query, top_k=10)
    output = {
        "persona": persona,
        "task": task,
        "relevant_sections": [],
        "final_summary": ""
    }

    combined_summary = []
    for section in top_sections:
        summary = summarize_text(section["text"])
        output["relevant_sections"].append({
            "pdf": section["pdf"],
            "page": section["page"],
            "content_summary": summary
        })
        combined_summary.append(summary)

    output["final_summary"] = "\n".join(combined_summary)

    Path(output_path).mkdir(parents=True, exist_ok=True)
    with open(Path(output_path) / "result.json", "w") as f:
        json.dump(output, f, indent=4)

    print("Output written to output/result.json")

if __name__ == "__main__":
    process("/app/input", "/app/persona_task.json", "/app/output")
