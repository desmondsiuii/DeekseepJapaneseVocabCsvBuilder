import os
import sys

def remove_lines_with_less_than_commas(input_file="task-result-accumulate.txt", min_commas=4):
    """
    Remove lines that have less than min_commas commas.
    No backup created - overwrites directly.
    """
    print("=" * 60)
    print("REMOVE LINES WITH LESS THAN 4 COMMAS")
    print("=" * 60)
    print(f"📁 Input file: {input_file}")
    print(f"📊 Minimum commas required: {min_commas}")
    
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
        
        # Filter lines with >= 4 commas
        kept_lines = []
        removed_count = 0
        
        for line in lines:
            original_line = line.rstrip('\n')
            comma_count = original_line.count(',')
            
            if comma_count >= min_commas:
                kept_lines.append(original_line)
            else:
                removed_count += 1
        
        print(f"   Lines kept (>= {min_commas} commas): {len(kept_lines)}")
        print(f"   Lines removed (< {min_commas} commas): {removed_count}")
        
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
    input_file = sys.argv[1] if len(sys.argv) > 1 else "task-result-accumulate.txt"
    min_commas = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    
    remove_lines_with_less_than_commas(input_file, min_commas)

if __name__ == "__main__":
    main()