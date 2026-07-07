from secret import DEEPSEEK_API_KEY
from openai import OpenAI

# Read and print entire file
for i in range(0, 1):
    with open('question.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    with open('summary.txt', 'r', encoding='utf-8') as f:
        summary_previous_answer = f.read()

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": content + summary_previous_answer},
        ],
        stream=False,
    )

    deepseek_api_response = response.choices[0].message.content
    
    with open('deepseek_api_task.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + deepseek_api_response)
