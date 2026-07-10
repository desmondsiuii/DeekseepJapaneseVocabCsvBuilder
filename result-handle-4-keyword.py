import os
import sys

def remove_lines_containing_keywords(input_file="task-result-accumulate.txt", keyword_file="keyword.txt"):
    """
    Remove lines from input_file that contain ANY of the keywords from keyword_file.
    Keywords should be comma-separated in keyword.txt.
    No backup created - overwrites directly.
    """
    print("=" * 60)
    print("LINE REMOVAL BY MULTIPLE KEYWORDS (OR logic)")
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
    
    # Read keywords
    try:
        with open(keyword_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        if not content:
            print("❌ Error: Keyword file is empty!")
            return False
        
        # Split by comma and clean up
        keywords = [kw.strip() for kw in content.split(',') if kw.strip()]
        print(f"📝 Keywords ({len(keywords)}): {', '.join(keywords)}")
    except Exception as e:
        print(f"❌ Error reading keyword file: {e}")
        return False
    
    try:
        # Read all lines
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("⚠️ File is empty")
            return True
        
        print(f"📊 Total lines: {len(lines)}")
        
        # Filter lines that don't contain any keyword
        kept_lines = []
        removed_count = 0
        
        for line in lines:
            original_line = line.rstrip('\n')
            should_remove = False
            
            # Check each keyword
            for kw in keywords:
                if kw in original_line:
                    should_remove = True
                    break
            
            if should_remove:
                removed_count += 1
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

def main():
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        keyword_file = sys.argv[2] if len(sys.argv) > 2 else "keyword.txt"
    else:
        input_file = "task-result-accumulate.txt"
        keyword_file = "keyword.txt"
    
    remove_lines_containing_keywords(input_file, keyword_file)

if __name__ == "__main__":
    main()