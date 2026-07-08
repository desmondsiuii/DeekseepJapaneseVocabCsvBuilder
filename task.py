from secret import DEEPSEEK_API_KEY
from openai import OpenAI

# Read and print entire file
for i in range(0, 1):
    with open('task-question.txt', 'r', encoding='utf-8') as f:
        question = f.read()
    with open('task-result-summary.txt', 'r', encoding='utf-8') as f:
        previous_task_result_summary = f.read()

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question + previous_task_result_summary},
        ],
        stream=False,
    )

    deepseek_api_response = response.choices[0].message.content
    
    with open('task-result.txt', 'w', encoding='utf-8') as f:
        f.write('\n' + deepseek_api_response)

    with open('task-question-substituted.txt', 'w', encoding='utf-8') as f:
        f.write(question + previous_task_result_summary)
        