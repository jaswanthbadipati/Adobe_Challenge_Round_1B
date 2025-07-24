import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def extract_relevant_content(config, pdf_dir):
    persona = config["persona"]["role"].lower()
    task = config["job_to_be_done"]["task"].lower()
    results = []

    for doc in config["documents"]:
        path = pdf_dir / doc["filename"]
        if not path.exists():
            continue
        text = extract_text_from_pdf(path)
        
        # Simple relevance: filter paragraphs mentioning keywords from task
        relevant_parts = []
        for para in text.split('\n'):
            if any(word in para.lower() for word in task.split()):
                relevant_parts.append(para.strip())

        results.append({
            "filename": doc["filename"],
            "title": doc["title"],
            "relevant_summary": "\n".join(relevant_parts[:10]) if relevant_parts else "No relevant content found."
        })

    return {
        "challenge_id": config["challenge_info"]["challenge_id"],
        "test_case_name": config["challenge_info"]["test_case_name"],
        "persona": config["persona"],
        "job_to_be_done": config["job_to_be_done"],
        "results": results
    }
