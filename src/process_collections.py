import os
import json
from pathlib import Path
from src.utils import extract_relevant_content

def process_all_collections():
    root_dir = Path(__file__).resolve().parent.parent
    for i in range(1, 4):
        collection_path = root_dir / f"collection {i}"
        input_file = collection_path / "challenge1b_input.json"
        output_file = collection_path / "challenge1b_output.json"
        pdf_dir = collection_path / "PDFs"

        if not input_file.exists():
            print(f"⚠️ Input file missing in {collection_path}")
            continue

        with open(input_file, 'r') as f:
            config = json.load(f)

        result = extract_relevant_content(config, pdf_dir)
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"✅ Processed Collection {i}: Output written to {output_file}")

if __name__ == "__main__":
    process_all_collections()
