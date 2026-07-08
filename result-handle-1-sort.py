import os
import sys
from datetime import datetime

def sort_file_by_first_column(input_file="task-result-accumulate.txt"):
    """
    Sort CSV file by first column and overwrite the original.
    Creates a backup before sorting.
    """
    print("=" * 60)
    print("CSV SORT UTILITY (by first column)")
    print("=" * 60)
    print(f"📁 Input file: {input_file}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    # Create backup
    backup_file = f"{input_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"📦 Backup created: {backup_file}")
    except Exception as e:
        print(f"⚠️ Could not create backup: {e}")
        response = input("Continue without backup? (y/n): ").lower()
        if response != 'y':
            print("❌ Operation cancelled")
            return False
    
    try:
        # Read all lines
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("⚠️ File is empty")
            return True
        
        # Parse lines into rows with first column
        rows = []
        for line in lines:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            parts = line.split(',')
            if parts:
                first_col = parts[0].strip()
                rows.append((first_col, line))
        
        if not rows:
            print("⚠️ No data rows found")
            return True
        
        print(f"📊 Found {len(rows)} rows")
        
        # Sort by first column (try numeric sort first, fallback to string sort)
        def sort_key(item):
            first_col = item[0]
            # Try numeric sorting
            try:
                return (0, float(first_col))
            except ValueError:
                try:
                    return (0, int(first_col))
                except ValueError:
                    return (1, first_col.lower())
        
        rows.sort(key=sort_key)
        
        # Get sorted lines
        sorted_lines = [row[1] + '\n' for row in rows]
        
        # Write back to original file
        with open(input_file, 'w', encoding='utf-8') as f:
            f.writelines(sorted_lines)
        
        print(f"✅ Sorted {len(sorted_lines)} lines by first column")
        print(f"   File overwritten: {input_file}")
        
        # Show sample of sorted data
        print("\n📋 First 10 lines after sorting:")
        print("-" * 40)
        for i, line in enumerate(sorted_lines[:10], 1):
            print(f"   {i}. {line.rstrip()}")
        if len(sorted_lines) > 10:
            print(f"   ... and {len(sorted_lines) - 10} more lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Error sorting file: {e}")
        return False

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "task-result-accumulate.txt"
    sort_file_by_first_column(input_file)

if __name__ == "__main__":
    main()