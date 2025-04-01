import csv
import json
import argparse
import re

"""
Anki to MiniAnki Flashcard Converter

This script converts Anki-exported CSV vocabulary files to JSON format 
Extracts hanzi, pinyin, English definitions, 
part of speech, and example sentences from Anki exports.

Usage:
    python parser.py input_file.csv output_file.json

Example:
    python parser.py Mandarin_Vocabulary_csv.csv flashcards.json

The output JSON file can be loaded directly into MiniAnki
"""

def parse_anki_csv_export(file_path):
    
    flashcards = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        
        for row in reader:
            # Skip empty rows or malformed data
            if not row or len(row) < 10:
                continue
            
            # Extract fields from the CSV
            index = row[0].strip()
            hanzi = row[1].strip()
            trad_hanzi = row[2].strip()  # Traditional form
            pinyin = row[3].strip()
            pinyin_num = row[4].strip()  # Numerical pinyin
            english = row[5].strip()
            part_of_speech = row[6].strip()
            
            # Extract example sentence
            example = ""
            # Look for Chinese example sentences with HTML tags
            for i in range(10, min(15, len(row))):
                if i < len(row) and row[i] and '<b>' in row[i]:
                    # Remove HTML tags to get clean text
                    example = re.sub(r'<[^>]+>', '', row[i])
                    break
            
            # Create flashcard dictionary
            flashcard = {
                'hanzi': hanzi,
                'pinyin': pinyin,
                'english': english,
                'part_of_speech': part_of_speech,
                'example': example,
                'interval': 300,
                'last_review': None,
                'review_count': 0
            }
            
            flashcards.append(flashcard)
    
    return flashcards

def main():
    parser = argparse.ArgumentParser(description='Convert Anki CSV export to JSON for MiniAnki')
    parser.add_argument('input_file', help='Path to the Anki export CSV file')
    parser.add_argument('output_file', help='Path for the output JSON file')
    
    args = parser.parse_args()
    
    try:
        flashcards = parse_anki_csv_export(args.input_file)
        
        # Save to JSON file
        with open(args.output_file, 'w', encoding='utf-8') as f:
            json.dump(flashcards, f, ensure_ascii=False, indent=2)
        
        print(f"Successfully converted {len(flashcards)} flashcards to {args.output_file}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()