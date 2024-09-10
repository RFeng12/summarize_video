key = "sk-i4HV3B69FYtMdi_EZ9cppaBG2aGFqVRakZsL1KYs9pT3BlbkFJcpcisdB9JDxoRV_VQkZtrx5kBj86Kc3mhnDK-Zp0sA"
from openai import OpenAI
client = OpenAI(api_key=key)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": 'write a paragraph answering the question: "what is an antelope?"',
        }
    ],
    model="gpt-4-1106-preview",
    max_tokens = 300
)

print(chat_completion.choices[0].message.content)
print(chat_completion)
