import os
import sys

def extract_words_before_first_comma(input_file, output_file="summary.txt"):
    """
    Read a file, extract the words before the first comma from each line,
    and write them to summary.txt (joined by commas).
    
    Args:
        input_file: Path to input file
        output_file: Output file (default: summary.txt)
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    # Read and process file
    extracted_words = []
    total_lines = 0
    empty_lines = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            original_line = line.rstrip('\n')
            
            # Extract words before first comma
            if ',' in original_line:
                words_before_comma = original_line.split(',', 1)[0].strip()
                if words_before_comma:  # Skip if empty
                    extracted_words.append(words_before_comma)
                else:
                    empty_lines += 1
            else:
                # No comma - use the whole line
                if original_line.strip():
                    extracted_words.append(original_line.strip())
                else:
                    empty_lines += 1
    
    # Join with commas and write to output file
    summary_content = ', '.join(extracted_words)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    # Print summary
    print(f"✅ Done!")
    print(f"   Input file: {input_file}")
    print(f"   Output file: {output_file}")
    print(f"   Total lines: {total_lines}")
    print(f"   Extracted words: {len(extracted_words)}")
    print(f"   Empty lines skipped: {empty_lines}")
    print(f"   Summary length: {len(summary_content)} characters")
    
    return True

def extract_words_before_first_comma_simple(input_file, output_file="summary.txt"):
    """
    Simpler version: outputs each extracted word on a new line instead of comma-separated.
    """
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return
    
    extracted_words = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Get words before first comma
            if ',' in line:
                word = line.split(',', 1)[0].strip()
            else:
                word = line
            
            if word:
                extracted_words.append(word)
    
    # Write to output file (one per line)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(extracted_words))
    
    print(f"✅ Extracted {len(extracted_words)} words to {output_file}")

def extract_and_format_custom(input_file, output_file="summary.txt", separator=", "):
    """
    Version with custom separator (default: comma+space)
    """
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return
    
    extracted_words = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # Get words before first comma
            if ',' in line:
                word = line.split(',', 1)[0].strip()
            else:
                word = line
            
            if word:
                extracted_words.append(word)
    
    # Join with custom separator
    result = separator.join(extracted_words)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✅ Done! {len(extracted_words)} words, {len(result)} characters")

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_before_comma.py <input_file> [output_file]")
        print("  input_file   : The file to process")
        print("  output_file  : Output file (default: summary.txt)")
        print("")
        print("Examples:")
        print("  python extract_before_comma.py data.csv")
        print("  python extract_before_comma.py data.csv output.txt")
        print("")
        print("This program extracts the words before the first comma in each line")
        print("and joins them with commas to create a summary.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "summary.txt"
    
    extract_words_before_first_comma(input_file, output_file)

if __name__ == "__main__":
    main()