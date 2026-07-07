import csv
import os

def sort_and_deduplicate_csv(input_file, output_file=None):
    """
    Read CSV file, sort by the words before the first comma,
    and remove duplicate lines.
    """
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_sorted_deduplicated{ext}"
    
    # Read all lines from CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    if not lines:
        print("❌ File is empty or contains no data")
        return False
    
    # Get header (first line)
    header = lines[0]
    data = lines[1:]
    
    # Remove duplicates based on the first column (before first comma)
    seen = set()
    unique_data = []
    
    for row in data:
        if row and row[0] not in seen:
            seen.add(row[0])
            unique_data.append(row)
    
    # Sort by the first column (case-insensitive)
    sorted_data = sorted(unique_data, key=lambda x: x[0].lower() if x else '')
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(sorted_data)
    
    print(f"✅ Done!")
    print(f"   Input file: {input_file}")
    print(f"   Output file: {output_file}")
    print(f"   Total rows: {len(lines)} (including header)")
    print(f"   Unique rows: {len(unique_data)}")
    print(f"   Duplicates removed: {len(data) - len(unique_data)}")
    print(f"   Sorted by: first column")
    
    return True

# Version: Without using csv module (manual split)
def sort_and_deduplicate_simple(input_file, output_file=None):
    """
    Simple version without csv module.
    Sorts by the word before the first comma.
    """
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_sorted_deduplicated{ext}"
    
    # Read lines
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        print("❌ File is empty")
        return False
    
    # Remove duplicates based on first column
    seen = set()
    unique_lines = []
    
    # Keep header
    header = lines[0]
    data = lines[1:]
    
    for line in data:
        # Get first column (everything before first comma)
        parts = line.split(',', 1)  # split at first comma only
        if parts:
            key = parts[0].strip()
            if key not in seen and key != '':
                seen.add(key)
                unique_lines.append(line)
    
    # Sort by first column
    sorted_data = sorted(unique_lines, key=lambda x: x.split(',', 1)[0].lower() if x.split(',', 1) else '')
    
    # Write output
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        f.write(header)
        f.writelines(sorted_data)
    
    print(f"✅ Done!")
    print(f"   Input: {input_file}")
    print(f"   Output: {output_file}")
    print(f"   Duplicates removed: {len(data) - len(sorted_data)}")
    print(f"   Unique rows: {len(sorted_data)}")
    
    return True

# Version with custom sort key (multiple columns)
def sort_and_deduplicate_advanced(input_file, output_file=None, sort_column=0):
    """
    Sort by any column and remove duplicates based on first column.
    
    Args:
        input_file: Input CSV file path
        output_file: Output file path (optional)
        sort_column: Column index to sort by (default: 0)
    """
    if output_file is None:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_sorted_deduplicated{ext}"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        lines = list(reader)
    
    if not lines:
        print("❌ File is empty")
        return False
    
    header = lines[0]
    data = lines[1:]
    
    # Remove duplicates based on first column
    seen = set()
    unique_data = []
    
    for row in data:
        if row and row[0] not in seen:
            seen.add(row[0])
            unique_data.append(row)
    
    # Sort by specified column
    sorted_data = sorted(unique_data, key=lambda x: x[sort_column].lower() if len(x) > sort_column and x[sort_column] else '')
    
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(sorted_data)
    
    print(f"✅ Done! Sorted by column {sort_column}")
    return True

# Main execution
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("CSV SORT AND DEDUPLICATE")
    print("=" * 60)
    
    # Check command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_file = input("Enter input CSV file name: ").strip()
        if not input_file:
            print("❌ No file specified")
            sys.exit(1)
        output_file = input("Enter output file name (press Enter for default): ").strip() or None
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    # Process the file
    sort_and_deduplicate_csv(input_file, output_file)