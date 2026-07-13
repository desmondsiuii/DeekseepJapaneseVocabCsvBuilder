import os
import sys
import csv
from datetime import datetime

def read_review_words(review_file="task-result-review.txt"):
    """
    Read Japanese vocab from task-result-review.txt (comma-separated)
    """
    try:
        with open(review_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                print(f"⚠️ task-result-review.txt is empty")
                return []
            # Split by comma and clean up
            words = [w.strip() for w in content.split(',') if w.strip()]
        print(f"✅ Read {len(words)} words from {review_file}")
        return words
    except FileNotFoundError:
        print(f"❌ File not found: {review_file}")
        return []
    except Exception as e:
        print(f"❌ Error reading {review_file}: {e}")
        return []

def find_matching_lines(data_file="task-result-accumulate.txt", review_words=None):
    """
    Find lines in data_file where 2nd column matches any review word.
    Returns a set of line numbers to remove.
    """
    if not review_words:
        print("⚠️ No review words provided")
        return set()
    
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return set()
    
    # Convert review words to a set for O(1) lookup
    review_set = set(review_words)
    lines_to_remove = set()
    total_lines = 0
    matched_lines = 0
    
    print(f"\n🔍 Scanning {data_file} for matches...")
    print(f"   Review words: {len(review_set)}")
    print("-" * 50)
    
    with open(data_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            total_lines += 1
            line = line.rstrip('\n')
            
            if not line.strip():
                continue
            
            # Split by comma and get 2nd column (index 1)
            parts = line.split(',')
            if len(parts) >= 2:
                second_col = parts[1].strip()
                if second_col in review_set:
                    lines_to_remove.add(line_num)
                    matched_lines += 1
                    # Show first few matches for preview
                    if matched_lines <= 10:
                        print(f"   Match {matched_lines}: Line {line_num} - '{second_col}'")
    
    if matched_lines > 10:
        print(f"   ... and {matched_lines - 10} more matches")
    
    print("-" * 50)
    print(f"📊 Scan complete:")
    print(f"   Total lines scanned: {total_lines}")
    print(f"   Lines to remove: {len(lines_to_remove)}")
    print(f"   Lines to keep: {total_lines - len(lines_to_remove)}")
    
    return lines_to_remove

def remove_lines(data_file="task-result-accumulate.txt", lines_to_remove=None, backup=True):
    """
    Remove specified lines from data_file.
    Creates a backup first if backup=True.
    """
    if not lines_to_remove:
        print("ℹ️ No lines to remove")
        return True
    
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        return False
    
    # Create backup
    # if backup:
    #     backup_file = f"{data_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    #     try:
    #         import shutil
    #         shutil.copy2(data_file, backup_file)
    #         print(f"📦 Backup created: {backup_file}")
    #     except Exception as e:
    #         print(f"⚠️ Could not create backup: {e}")
    #         response = input("Continue without backup? (y/n): ").lower()
    #         if response != 'y':
    #             print("❌ Operation cancelled")
    #             return False
    
    # Read all lines
    with open(data_file, 'r', encoding='utf-8') as f:
        all_lines = f.readlines()
    
    # Remove specified lines (1-indexed)
    keep_lines = []
    for i, line in enumerate(all_lines, 1):
        if i not in lines_to_remove:
            keep_lines.append(line)
    
    # Write back
    try:
        with open(data_file, 'w', encoding='utf-8') as f:
            f.writelines(keep_lines)
        print(f"✅ Removed {len(lines_to_remove)} lines from {data_file}")
        print(f"   New file size: {len(keep_lines)} lines")
        return True
    except Exception as e:
        print(f"❌ Error writing to file: {e}")
        return False

def process_removal_with_summary(review_file="task-result-review.txt", data_file="task-result-accumulate.txt"):
    """
    Complete process: read task-result-review.txt, find matches, remove lines from data file.
    """
    print("=" * 60)
    print("JAPANESE VOCAB REMOVAL TOOL")
    print("=" * 60)
    print(f"📖 Review file: {review_file}")
    print(f"📁 Data file: {data_file}")
    print("=" * 60)
    
    # Step 1: Read review words
    review_words = read_review_words(review_file)
    if not review_words:
        print("❌ No words to process. Exiting.")
        return False
    
    print(f"📝 Words to remove: {', '.join(review_words[:10])}")
    if len(review_words) > 10:
        print(f"   ... and {len(review_words) - 10} more")
    
    # Step 2: Find matching lines
    lines_to_remove = find_matching_lines(data_file, review_words)
    
    if not lines_to_remove:
        print("\n✅ No matches found. Nothing to remove.")
        return True
    
    # Step 3: Preview removal
    print("\n" + "=" * 60)
    print("📋 REMOVAL SUMMARY")
    print("=" * 60)
    print(f"   Lines to remove: {len(lines_to_remove)}")
    print(f"   Lines to keep: {os.path.getsize(data_file) - len(lines_to_remove)} (approx)")
    
    # Show some lines to remove (preview)
    sorted_lines = sorted(lines_to_remove)
    print("\n   First 10 lines to remove:")
    for line_num in sorted_lines[:10]:
        print(f"      Line {line_num}")
    if len(sorted_lines) > 10:
        print(f"      ... and {len(sorted_lines) - 10} more")
    
    # Step 4: Confirm
    print("\n⚠️  WARNING: This will permanently remove lines from the data file!")
    confirm = input("Proceed with removal? (yes/no): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Operation cancelled")
        return False
    
    # Step 5: Remove lines
    success = remove_lines(data_file, lines_to_remove, backup=True)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ REMOVAL COMPLETED SUCCESSFULLY!")
        print("=" * 60)
    else:
        print("\n❌ Removal failed!")
    
    return success

def main():
    # Parse command line arguments
    review_file = "task-result-review.txt"
    data_file = "task-result-accumulate.txt"
    
    if len(sys.argv) > 1:
        review_file = sys.argv[1]
    if len(sys.argv) > 2:
        data_file = sys.argv[2]
    
    process_removal_with_summary(review_file, data_file)

if __name__ == "__main__":
    main()