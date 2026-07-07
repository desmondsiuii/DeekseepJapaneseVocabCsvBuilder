import os
import sys

def filter_lines_by_commas(input_file, min_commas=4, outstand_file="outstand.txt", filtered_file="filtered.txt"):
    """
    Read a file and split lines based on comma count.
    - Lines with > min_commas commas -> outstand.txt
    - Lines with <= min_commas commas -> filtered.txt
    
    Args:
        input_file: Path to input file
        min_commas: Minimum number of commas to trigger (default: 4)
        outstand_file: Output file for lines with > min_commas commas
        filtered_file: Output file for lines with <= min_commas commas
    """
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: File '{input_file}' not found!")
        return False
    
    # Read and process file
    outstanding_lines = []
    filtered_lines = []
    total_lines = 0
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            original_line = line.rstrip('\n')
            
            # Count commas
            comma_count = original_line.count(',')
            
            if comma_count > min_commas:
                outstanding_lines.append({
                    'line_num': line_num,
                    'comma_count': comma_count,
                    'content': original_line
                })
            else:
                filtered_lines.append(original_line)
    
    # Write outstanding lines to outstand.txt
    with open(outstand_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"LINES WITH MORE THAN {min_commas} COMMAS\n")
        f.write(f"Source file: {input_file}\n")
        f.write(f"Total lines: {len(outstanding_lines)}\n")
        f.write("=" * 70 + "\n\n")
        
        for item in outstanding_lines:
            f.write(f"Line {item['line_num']:6d} | Commas: {item['comma_count']:2d} | {item['content']}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Total: {len(outstanding_lines)} lines\n")
        f.write("=" * 70 + "\n")
    
    # Write filtered lines to filtered.txt
    with open(filtered_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write(f"FILTERED LINES (≤ {min_commas} COMMAS)\n")
        f.write(f"Source file: {input_file}\n")
        f.write(f"Total lines: {len(filtered_lines)}\n")
        f.write("=" * 70 + "\n\n")
        
        for line in filtered_lines:
            f.write(line + '\n')
        
        f.write("\n" + "=" * 70 + "\n")
        f.write(f"Total: {len(filtered_lines)} lines\n")
        f.write("=" * 70 + "\n")
    
    # Print summary
    print(f"✅ Done!")
    print(f"   Input file: {input_file}")
    print(f"   Total lines: {total_lines}")
    print(f"   📤 Lines with >{min_commas} commas: {len(outstanding_lines)} -> {outstand_file}")
    print(f"   📥 Lines with ≤{min_commas} commas: {len(filtered_lines)} -> {filtered_file}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python filter_by_commas.py <input_file> [min_commas]")
        print("  input_file   : The file to process")
        print("  min_commas   : Minimum commas to trigger (default: 4)")
        print("")
        print("Output files:")
        print("  outstand.txt  : Lines with > min_commas commas")
        print("  filtered.txt  : Lines with ≤ min_commas commas")
        print("")
        print("Examples:")
        print("  python filter_by_commas.py data.csv")
        print("  python filter_by_commas.py data.csv 5")
        sys.exit(1)
    
    input_file = sys.argv[1]
    min_commas = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    
    filter_lines_by_commas(input_file, min_commas)

if __name__ == "__main__":
    main()