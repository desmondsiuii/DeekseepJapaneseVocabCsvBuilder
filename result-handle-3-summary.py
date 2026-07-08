import os
import sys

def extract_words_before_second_comma(input_file, output_file="task-result-summary.txt"):
    """
    Read a file, extract the words before the second comma from each line,
    and write them to task-result-summary.txt (joined by commas).
    
    Args:
        input_file: Path to input file
        output_file: Output file (default: task-result-summary.txt)
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    # Read and process file
    extracted_words = []
    total_lines = 0
    empty_lines = 0
    skipped_lines = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            original_line = line.rstrip('\n')
            
            # Extract words before the second comma
            parts = original_line.split(',')
            
            if len(parts) >= 2:
                # Get the second column (index 1)
                second_col = parts[1].strip()
                if second_col:
                    extracted_words.append(second_col)
                else:
                    empty_lines += 1
            else:
                # Less than 2 columns - skip or use whole line
                if original_line.strip():
                    # Option 1: Skip lines without 2 columns
                    skipped_lines += 1
                    # Option 2: Use the whole line
                    # extracted_words.append(original_line.strip())
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
    print(f"   Extracted words (2nd column): {len(extracted_words)}")
    print(f"   Empty lines skipped: {empty_lines}")
    print(f"   Lines without 2nd column: {skipped_lines}")
    print(f"   Summary length: {len(summary_content)} characters")
    
    return True

def extract_words_from_column(input_file, column_index=1, output_file="task-result-summary.txt"):
    """
    Extract words from a specific column (0-based index).
    
    Args:
        input_file: Path to input file
        column_index: Column index to extract (0 = first, 1 = second, etc.)
        output_file: Output file (default: task-result-summary.txt)
    """
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    extracted_words = []
    total_lines = 0
    skipped_lines = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            original_line = line.rstrip('\n')
            
            if not original_line.strip():
                continue
            
            parts = original_line.split(',')
            
            if len(parts) > column_index:
                word = parts[column_index].strip()
                if word:
                    extracted_words.append(word)
                else:
                    skipped_lines += 1
            else:
                skipped_lines += 1
    
    # Join with commas and write to output file
    summary_content = ', '.join(extracted_words)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
    
    print(f"✅ Done!")
    print(f"   Input file: {input_file}")
    print(f"   Output file: {output_file}")
    print(f"   Column used: {column_index + 1} (0-based: {column_index})")
    print(f"   Total lines: {total_lines}")
    print(f"   Extracted words: {len(extracted_words)}")
    print(f"   Skipped lines: {skipped_lines}")
    print(f"   Summary length: {len(summary_content)} characters")
    
    return True

def extract_words_before_second_comma_simple(input_file, output_file="task-result-summary.txt"):
    """
    Simpler version: outputs each extracted word on a new line instead of comma-separated.
    Uses the 2nd column.
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
            
            parts = line.split(',')
            if len(parts) >= 2:
                word = parts[1].strip()
                if word:
                    extracted_words.append(word)
    
    # Write to output file (one per line)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(extracted_words))
    
    print(f"✅ Extracted {len(extracted_words)} words to {output_file}")

def extract_and_format_custom(input_file, output_file="task-result-summary.txt", separator=", ", column_index=1):
    """
    Version with custom separator and column selection.
    
    Args:
        input_file: Path to input file
        output_file: Output file (default: task-result-summary.txt)
        separator: Separator for output (default: ", ")
        column_index: Column to extract (0 = first, 1 = second, etc.)
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
            
            parts = line.split(',')
            if len(parts) > column_index:
                word = parts[column_index].strip()
                if word:
                    extracted_words.append(word)
    
    # Join with custom separator
    result = separator.join(extracted_words)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"✅ Done! {len(extracted_words)} words, {len(result)} characters")

def main():
    if len(sys.argv) < 2:
        print("=" * 60)
        print("CSV COLUMN EXTRACTOR")
        print("=" * 60)
        print("Usage: python summary.py <input_file> [output_file] [column_index]")
        print("  input_file   : The file to process")
        print("  output_file  : Output file (default: task-result-summary.txt)")
        print("  column_index : Column to extract (0 = first, 1 = second, default: 1)")
        print("")
        print("Examples:")
        print("  python summary.py data.csv                      # Uses 2nd column")
        print("  python summary.py data.csv output.txt          # Uses 2nd column")
        print("  python summary.py data.csv output.txt 0        # Uses 1st column")
        print("  python summary.py data.csv output.txt 2        # Uses 3rd column")
        print("")
        print("This program extracts words from the specified column")
        print("and joins them with commas to create a summary.")
        print("=" * 60)
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "task-result-summary.txt"
    column_index = int(sys.argv[3]) if len(sys.argv) > 3 else 1  # Default to 2nd column
    
    # Use the column-based extractor
    extract_words_from_column(input_file, column_index, output_file)

if __name__ == "__main__":
    main()