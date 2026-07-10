import os
import sys
from datetime import datetime

def remove_lines_containing_keyword(input_file="task-result-accumulate.txt", keyword_file="keyword.txt"):
    """
    Remove lines from input_file that contain the keyword from keyword_file.
    Creates a backup before removal.
    """
    print("=" * 60)
    print("LINE REMOVAL BY KEYWORD")
    print("=" * 60)
    print(f"📁 Input file: {input_file}")
    print(f"📄 Keyword file: {keyword_file}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    # Check if keyword file exists
    if not os.path.exists(keyword_file):
        print(f"❌ Error: Keyword file '{keyword_file}' not found!")
        return False
    
    # Read keyword
    try:
        with open(keyword_file, 'r', encoding='utf-8') as f:
            keyword = f.read().strip()
        if not keyword:
            print("❌ Error: Keyword file is empty!")
            return False
        print(f"📝 Keyword: '{keyword}'")
    except Exception as e:
        print(f"❌ Error reading keyword file: {e}")
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
        
        print(f"📊 Total lines: {len(lines)}")
        
        # Filter lines that don't contain the keyword
        kept_lines = []
        removed_count = 0
        
        for line in lines:
            original_line = line.rstrip('\n')
            if keyword in original_line:
                removed_count += 1
                print(f"   Removed: {original_line[:50]}...") if len(original_line) > 50 else print(f"   Removed: {original_line}")
            else:
                kept_lines.append(original_line)
        
        print(f"   Lines kept: {len(kept_lines)}")
        print(f"   Lines removed: {removed_count}")
        
        # Write back to file
        with open(input_file, 'w', encoding='utf-8') as f:
            for line in kept_lines:
                f.write(line + '\n')
        
        print(f"✅ File updated: {input_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def remove_lines_containing_keyword_simple(input_file="task-result-accumulate.txt", keyword_file="keyword.txt"):
    """
    Simpler version without backup and preview.
    """
    try:
        # Read keyword
        with open(keyword_file, 'r', encoding='utf-8') as f:
            keyword = f.read().strip()
        
        if not keyword:
            print("❌ Keyword file is empty!")
            return False
        
        print(f"📝 Removing lines containing: '{keyword}'")
        
        # Read and filter
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        kept_lines = []
        removed_count = 0
        
        for line in lines:
            if keyword not in line:
                kept_lines.append(line.rstrip('\n'))
            else:
                removed_count += 1
        
        # Write back
        with open(input_file, 'w', encoding='utf-8') as f:
            for line in kept_lines:
                f.write(line + '\n')
        
        print(f"✅ Removed {removed_count} lines containing '{keyword}'")
        print(f"   {len(kept_lines)} lines kept")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        keyword_file = sys.argv[2] if len(sys.argv) > 2 else "keyword.txt"
    else:
        input_file = "task-result-accumulate.txt"
        keyword_file = "keyword.txt"
    
    remove_lines_containing_keyword(input_file, keyword_file)

if __name__ == "__main__":
    main()