import csv
import sys
from collections import Counter

def read_column_2(filename):
    """
    Read column 2 (index 1) from a CSV file and return a list of values.
    """
    values = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row_num, row in enumerate(reader, 1):
                if len(row) >= 2:
                    col2_value = row[1].strip()
                    if col2_value:  # Skip empty values
                        values.append(col2_value)
                else:
                    print(f"⚠️ Row {row_num} in {filename} has less than 2 columns: {row}")
        print(f"✅ Read {len(values)} values from column 2 of {filename}")
        return values
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return []
    except Exception as e:
        print(f"❌ Error reading {filename}: {e}")
        return []

def find_duplicates_between_files(para1_values, para2_values):
    """
    Find values that appear in both para1 and para2 (duplicates between files).
    """
    # Convert to sets for O(1) lookup
    set1 = set(para1_values)
    set2 = set(para2_values)
    
    # Find intersection (values in both files)
    duplicates = set1.intersection(set2)
    
    return duplicates

def find_duplicates_within_file(values, filename):
    """
    Find duplicates within a single file.
    """
    counts = Counter(values)
    duplicates = {value: count for value, count in counts.items() if count > 1}
    return duplicates

def find_all_duplicates(para1_values, para2_values):
    """
    Comprehensive duplicate analysis:
    1. Values duplicated between files
    2. Values duplicated within para1
    3. Values duplicated within para2
    """
    # Between files
    set1 = set(para1_values)
    set2 = set(para2_values)
    between_files = set1.intersection(set2)
    
    # Within para1
    counts1 = Counter(para1_values)
    within_para1 = {v: c for v, c in counts1.items() if c > 1}
    
    # Within para2
    counts2 = Counter(para2_values)
    within_para2 = {v: c for v, c in counts2.items() if c > 1}
    
    return {
        'between_files': between_files,
        'within_para1': within_para1,
        'within_para2': within_para2
    }

def print_analysis(para1_values, para2_values):
    """
    Print comprehensive analysis results.
    """
    print("\n" + "=" * 60)
    print("DUPLICATE ANALYSIS")
    print("=" * 60)
    
    # Basic stats
    print(f"📊 Statistics:")
    print(f"   para1: {len(para1_values)} values")
    print(f"   para2: {len(para2_values)} values")
    print(f"   Unique in para1: {len(set(para1_values))}")
    print(f"   Unique in para2: {len(set(para2_values))}")
    
    # Get duplicates
    results = find_all_duplicates(para1_values, para2_values)
    
    # Duplicates within para1
    print(f"\n📋 Duplicates WITHIN para1:")
    if results['within_para1']:
        for value, count in sorted(results['within_para1'].items()):
            print(f"   '{value}' appears {count} times")
    else:
        print("   No duplicates found")
    
    # Duplicates within para2
    print(f"\n📋 Duplicates WITHIN para2:")
    if results['within_para2']:
        for value, count in sorted(results['within_para2'].items()):
            print(f"   '{value}' appears {count} times")
    else:
        print("   No duplicates found")
    
    # Duplicates between files
    print(f"\n📋 Duplicates BETWEEN para1 and para2:")
    if results['between_files']:
        for value in sorted(results['between_files']):
            # Count occurrences in each file
            count1 = para1_values.count(value)
            count2 = para2_values.count(value)
            print(f"   '{value}' (para1: {count1}x, para2: {count2}x)")
    else:
        print("   No duplicates found")
    
    print("\n" + "=" * 60)

def save_duplicates_to_file(para1_values, para2_values, output_file="duplicates.txt"):
    """
    Save duplicate analysis to a file.
    """
    results = find_all_duplicates(para1_values, para2_values)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("DUPLICATE ANALYSIS RESULTS\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"para1: {len(para1_values)} values\n")
        f.write(f"para2: {len(para2_values)} values\n")
        f.write(f"Unique in para1: {len(set(para1_values))}\n")
        f.write(f"Unique in para2: {len(set(para2_values))}\n\n")
        
        # Duplicates within para1
        f.write("DUPLICATES WITHIN para1:\n")
        f.write("-" * 40 + "\n")
        if results['within_para1']:
            for value, count in sorted(results['within_para1'].items()):
                f.write(f"  '{value}' appears {count} times\n")
        else:
            f.write("  No duplicates found\n")
        f.write("\n")
        
        # Duplicates within para2
        f.write("DUPLICATES WITHIN para2:\n")
        f.write("-" * 40 + "\n")
        if results['within_para2']:
            for value, count in sorted(results['within_para2'].items()):
                f.write(f"  '{value}' appears {count} times\n")
        else:
            f.write("  No duplicates found\n")
        f.write("\n")
        
        # Duplicates between files
        f.write("DUPLICATES BETWEEN para1 AND para2:\n")
        f.write("-" * 40 + "\n")
        if results['between_files']:
            for value in sorted(results['between_files']):
                count1 = para1_values.count(value)
                count2 = para2_values.count(value)
                f.write(f"  '{value}' (para1: {count1}x, para2: {count2}x)\n")
        else:
            f.write("  No duplicates found\n")
        f.write("\n")
        
        f.write("=" * 60 + "\n")
    
    print(f"✅ Results saved to: {output_file}")

def main():
    if len(sys.argv) < 3:
        print("=" * 60)
        print("COLUMN 2 DUPLICATE FINDER")
        print("=" * 60)
        print("Usage:")
        print(f"  python {sys.argv[0]} <para1.csv> <para2.csv> [options]")
        print("")
        print("Options:")
        print("  -o, --output <file>  Output file for results (default: duplicates.txt)")
        print("  -s, --save           Save results to file")
        print("  -h, --help           Show this help")
        print("")
        print("Example:")
        print(f"  python {sys.argv[0]} para1.csv para2.csv")
        print(f"  python {sys.argv[0]} para1.csv para2.csv -o results.txt")
        print("=" * 60)
        sys.exit(1)
    
    para1_file = sys.argv[1]
    para2_file = sys.argv[2]
    
    # Parse options
    save_output = False
    output_file = "duplicates.txt"
    
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] in ['-o', '--output'] and i + 1 < len(sys.argv):
            output_file = sys.argv[i + 1]
            save_output = True
            i += 2
        elif sys.argv[i] in ['-s', '--save']:
            save_output = True
            i += 1
        elif sys.argv[i] in ['-h', '--help']:
            print("Help...")
            sys.exit(0)
        else:
            i += 1
    
    # Read column 2 from both files
    para1_values = read_column_2(para1_file)
    para2_values = read_column_2(para2_file)
    
    if not para1_values or not para2_values:
        print("❌ Could not read one or both files")
        sys.exit(1)
    
    # Print analysis
    print_analysis(para1_values, para2_values)
    
    # Save if requested
    if save_output:
        save_duplicates_to_file(para1_values, para2_values, output_file)

if __name__ == "__main__":
    main()