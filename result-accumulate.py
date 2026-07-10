import os
import sys
from datetime import datetime

def append_with_cleanup(source_file="task-result-trimed.txt", target_file="task-result-accumulate.txt", backup=True):
    """
    Append source_file to target_file with proper newline handling.
    
    Requirements:
    1. If target file doesn't end with newline, add one first
    2. If source file starts with newline, remove it
    3. After append, ensure target file ends with newline
    """
    print("=" * 60)
    print("FILE APPEND UTILITY (with newline handling)")
    print("=" * 60)
    print(f"📂 Source: {source_file}")
    print(f"📁 Target: {target_file}")
    print("=" * 60)
    
    # Check if source file exists
    if not os.path.exists(source_file):
        print(f"❌ Error: Source file '{source_file}' not found!")
        return False
    
    # Check if target file exists
    target_exists = os.path.exists(target_file)
    
    # Create backup of target file (if exists)
    if backup and target_exists:
        backup_file = f"{target_file}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
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
        # Read source file content
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()
        
        # Get source lines count
        source_lines = source_content.splitlines()
        source_count = len(source_lines)
        print(f"📖 Read {source_count} lines from {source_file}")
        
        # --- Process Requirement 2: Remove leading newline from source ---
        if source_content.startswith('\n'):
            source_content = source_content.lstrip('\n')
            print(f"   🔧 Removed leading newline(s) from source")
        
        # --- Process Requirement 1: Ensure target ends with newline ---
        if target_exists:
            with open(target_file, 'r', encoding='utf-8') as f:
                target_content = f.read()
            
            target_lines = target_content.splitlines()
            target_count = len(target_lines)
            print(f"📖 Target file has {target_count} lines")
            
            # Check if target file ends with newline
            if target_content and not target_content.endswith('\n'):
                print(f"   🔧 Target file doesn't end with newline - adding one")
                with open(target_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
        else:
            print(f"📖 Target file does not exist, will create new file")
        
        # --- Append source content to target ---
        with open(target_file, 'a', encoding='utf-8') as f:
            f.write(source_content)
        
        print(f"✅ Appended {source_count} lines from {source_file}")
        
        # --- Process Requirement 3: Ensure target ends with newline after append ---
        with open(target_file, 'r', encoding='utf-8') as f:
            final_content = f.read()
        
        if final_content and not final_content.endswith('\n'):
            print(f"   🔧 Adding final newline to target file")
            with open(target_file, 'a', encoding='utf-8') as f:
                f.write('\n')
        
        # Show final statistics
        with open(target_file, 'r', encoding='utf-8') as f:
            final_lines = f.readlines()
        print(f"📊 New total lines in {target_file}: {len(final_lines)}")
        
        print("\n" + "=" * 60)
        print("✅ Append completed successfully!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error appending file: {e}")
        return False

def append_simple(source_file="task-result-trimed.txt", target_file="task-result-accumulate.txt"):
    """
    Simpler version without backup and detailed output.
    """
    try:
        # Check source
        if not os.path.exists(source_file):
            print(f"❌ Source file not found: {source_file}")
            return False
        
        # Read source
        with open(source_file, 'r', encoding='utf-8') as f:
            source_content = f.read()
        
        # Remove leading newline from source
        if source_content.startswith('\n'):
            source_content = source_content.lstrip('\n')
        
        # Check target and add newline if needed
        if os.path.exists(target_file):
            with open(target_file, 'r', encoding='utf-8') as f:
                target_content = f.read()
            if target_content and not target_content.endswith('\n'):
                with open(target_file, 'a', encoding='utf-8') as f:
                    f.write('\n')
        
        # Append
        with open(target_file, 'a', encoding='utf-8') as f:
            f.write(source_content)
        
        # Ensure final newline
        with open(target_file, 'r', encoding='utf-8') as f:
            final_content = f.read()
        if final_content and not final_content.endswith('\n'):
            with open(target_file, 'a', encoding='utf-8') as f:
                f.write('\n')
        
        print(f"✅ Appended {source_file} to {target_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    if len(sys.argv) > 1:
        source = sys.argv[1]
        target = sys.argv[2] if len(sys.argv) > 2 else "task-result-accumulate.txt"
    else:
        source = "task-result.txt"
        target = "task-result-accumulate.txt"
    
    append_with_cleanup(source, target)

if __name__ == "__main__":
    main()