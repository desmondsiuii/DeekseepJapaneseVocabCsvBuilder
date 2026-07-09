import os
import sys
import re

def is_hiragana_start(text):
    """
    Check if text starts with a Japanese Hiragana character.
    Hiragana Unicode range: U+3040 to U+309F
    """
    if not text or not text.strip():
        return False
    first_char = text.strip()[0]
    # Hiragana Unicode range
    return 0x3040 <= ord(first_char) <= 0x309F

def filter_hiragana_lines(input_file="task-result.txt"):
    """
    Remove lines that don't start with Hiragana.
    Overwrites the original file.
    """
    print("=" * 60)
    print("HIRAGANA LINE FILTER")
    print("=" * 60)
    print(f"📁 Input file: {input_file}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    try:
        # Read all lines
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            print("⚠️ File is empty")
            return True
        
        print(f"📊 Total lines: {len(lines)}")
        
        # Filter lines that start with Hiragana
        kept_lines = []
        removed_count = 0
        
        for line in lines:
            original_line = line.rstrip('\n')
            
            # Split by comma and get first field
            parts = original_line.split(',')
            if parts:
                first_field = parts[0].strip()
                if is_hiragana_start(first_field):
                    kept_lines.append(original_line)
                else:
                    removed_count += 1
            else:
                # If no comma, check the whole line
                if is_hiragana_start(original_line):
                    kept_lines.append(original_line)
                else:
                    removed_count += 1
        
        print(f"   Lines kept: {len(kept_lines)}")
        print(f"   Lines removed: {removed_count}")
        
        # Add newline at the end if not already present
        if kept_lines:
            # Write back to file
            with open(input_file, 'w', encoding='utf-8') as f:
                for line in kept_lines:
                    f.write(line + '\n')
            
            # Ensure file ends with newline
            with open(input_file, 'a', encoding='utf-8') as f:
                f.write('')
        
        print(f"✅ File updated: {input_file}")
        
        # Show sample of kept lines
        print("\n📋 First 10 kept lines:")
        print("-" * 40)
        for i, line in enumerate(kept_lines[:10], 1):
            parts = line.split(',')
            if parts:
                first_field = parts[0]
                print(f"   {i}. {first_field}...")
        if len(kept_lines) > 10:
            print(f"   ... and {len(kept_lines) - 10} more lines")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "task-result.txt"
    filter_hiragana_lines(input_file)

if __name__ == "__main__":
    main()