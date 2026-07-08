import os
import sys
from openai import OpenAI
from secret import DEEPSEEK_API_KEY  # Make sure you have this

def read_vocab_from_file(filename="summary.txt"):
    """Read Japanese vocab from file, separated by comma"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Split by comma and clean up
            vocab_list = [v.strip() for v in content.split(',') if v.strip()]
        print(f"✅ Read {len(vocab_list)} vocab items from {filename}")
        return vocab_list
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
        return []
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return []

def ask_deepseek(vocab_list):
    """Send vocab to DeepSeek API and get response"""
    
    # Check if API key is available
    if not DEEPSEEK_API_KEY:
        print("❌ DEEPSEEK_API_KEY not found in config.py")
        return None
    
    # Create prompt
    vocab_str = ", ".join(vocab_list)
    
    prompt = f"""You are a Japanese language expert. I have a list of Japanese vocabulary words separated by commas:

{vocab_str}

Please do the following:
1. Identify which of these words are NOT verbs (i.e., they are nouns, adjectives, adverbs, etc.)
2. Put a brief greeting or explanation on LINE 1 of your response.
3. On LINE 2, put ONLY the non-verb words, separated by commas. Do NOT put anything else on LINE 2.

Example format:
LINE 1: Here are the non-verb words I found:
LINE 2: 学校, 大きい, 速く

Return ONLY these two lines, nothing else."""

    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        
        print("🤖 Sending request to DeepSeek API...")
        
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "You are a Japanese language expert. Always respond in exactly two lines as specified."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
        )
        
        result = response.choices[0].message.content
        print("✅ Received response from DeepSeek")
        return result
        
    except Exception as e:
        print(f"❌ Error calling DeepSeek API: {e}")
        return None

def process_response(response, output_file="task-result-review.txt"):
    """Process the response and extract line 2 to output file"""
    if not response:
        print("❌ No response to process")
        return False
    
    lines = response.strip().split('\n')
    
    # Remove empty lines
    lines = [line for line in lines if line.strip()]
    
    if len(lines) < 2:
        print(f"⚠️ Response has less than 2 lines. Full response:")
        print(response)
        print("\nSaving full response to task-result-review.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response)
        return True
    
    # Extract line 2 (index 1)
    line1 = lines[0]
    line2 = lines[1]
    
    print("\n" + "=" * 50)
    print("📋 Response from DeepSeek:")
    print("-" * 50)
    print(f"Line 1 (greeting/explanation): {line1}")
    print(f"Line 2 (non-verb words): {line2}")
    print("=" * 50)
    
    # Save only line 2 to task-result-review.txt
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(line2)
        print(f"✅ Saved non-verb words to {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving to file: {e}")
        return False

def main():
    print("=" * 60)
    print("JAPANESE VOCAB FILTER (NON-VERBS)")
    print("=" * 60)
    
    # Read vocab from summary.txt
    vocab_list = read_vocab_from_file("summary.txt")
    
    if not vocab_list:
        print("❌ No vocabulary found. Please check summary.txt")
        print("   File should contain Japanese words separated by commas")
        sys.exit(1)
    
    print(f"📝 Vocab to check: {vocab_list}")
    print("-" * 60)
    
    # Ask DeepSeek
    response = ask_deepseek(vocab_list)
    
    if not response:
        print("❌ Failed to get response from DeepSeek")
        sys.exit(1)
    
    # Process and save
    process_response(response, "task-result-review.txt")
    
    print("\n" + "=" * 60)
    print("✅ Done!")

if __name__ == "__main__":
    main()