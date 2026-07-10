import os
import sys
from datetime import datetime

def deduplicate_by_second_column(input_file="task-result-accumulate.txt"):
    """
    Remove duplicate lines based on the 2nd column (keep first occurrence).
    Creates a backup before deduplication.
    """
    print("=" * 60)
    print("CSV DEDUPLICATE UTILITY (by 2nd column)")
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
        # with open(backup_file, 'w', encoding='utf-8') as f:
        #     f.write(content)
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
        
        # Deduplicate by 2nd column
        seen = set()
        unique_lines = []
        duplicate_count = 0
        
        for line in lines:
            line = line.rstrip('\n')
            if not line.strip():
                unique_lines.append(line)  # Keep empty lines
                continue
            
            parts = line.split(',')
            if len(parts) >= 2:
                second_col = parts[1].strip()
                if second_col not in seen:
                    seen.add(second_col)
                    unique_lines.append(line)
                else:
                    duplicate_count += 1
            else:
                # Lines without 2nd column are kept (no way to deduplicate)
                unique_lines.append(line)
        
        print(f"📊 Found {len(lines)} lines")
        print(f"   Unique lines: {len(unique_lines)}")
        print(f"   Duplicates removed: {duplicate_count}")
        
        # Write back to original file
        with open(input_file, 'w', encoding='utf-8') as f:
            for line in unique_lines:
                f.write(line + '\n')
        
        print(f"✅ Deduplication complete!")
        print(f"   File overwritten: {input_file}")
        
        # Show sample of deduplicated data
        print("\n📋 First 10 lines after deduplication:")
        print("-" * 40)
        for i, line in enumerate(unique_lines[:10], 1):
            parts = line.split(',')
            if len(parts) >= 2:
                print(f"   {i}. {parts[0]},{parts[1]},...")
            else:
                print(f"   {i}. {line}")
        if len(unique_lines) > 10:
            print(f"   ... and {len(unique_lines) - 10} more lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Error deduplicating file: {e}")
        return False

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "task-result-accumulate.txt"
    deduplicate_by_second_column(input_file)

if __name__ == "__main__":
    main()