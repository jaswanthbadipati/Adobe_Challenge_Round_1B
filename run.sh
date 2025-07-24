#!/bin/bash
echo "🔁 Installing dependencies..."
pip install -r requirements.txt

echo "🚀 Running PDF Processor for Challenge 1B..."
python3 src/process_collections.py
