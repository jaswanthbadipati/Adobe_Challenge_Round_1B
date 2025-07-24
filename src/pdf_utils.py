import fitz  # PyMuPDF

def extract_headings(pdf_path, persona, task, top_n=5):
    doc = fitz.open(pdf_path)
    candidates = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                spans = line["spans"]
                text = " ".join(span["text"] for span in spans).strip()
                if not text or len(text) < 10:
                    continue
                font_size = max(span["size"] for span in spans)
                candidates.append((font_size, text, page_num))

    # Sort and deduplicate
    candidates = sorted(candidates, key=lambda x: (-x[0], x[2]))  # by font size then page
    seen = set()
    top_sections = []
    for rank, (font_size, text, page) in enumerate(candidates[:top_n]):
        if text in seen:
            continue
        seen.add(text)
        top_sections.append({
            "section_title": text,
            "importance_rank": rank + 1,
            "page_number": page
        })

    return top_sections


def extract_relevant_paragraphs(pdf_path, persona, task):
    doc = fitz.open(pdf_path)
    key_terms = set(persona.lower().split() + task.lower().split())
    results = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        for para in text.split("\n\n"):
            if not para or len(para.split()) < 20:
                continue
            if any(word in para.lower() for word in key_terms):
                results.append({
                    "refined_text": para.strip(),
                    "page_number": page_num
                })
    return results[:5]  # limit to top 5
