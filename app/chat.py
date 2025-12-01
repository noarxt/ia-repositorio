import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("🤖 IA pronta pra conversar! (digite 'sair' pra encerrar)\n")

while True:
    user_input = input("Você: ")

    if user_input.lower() == "sair":
        print("IA: até mais 👋")
        break

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  
        messages=[{"role": "user", "content": user_input}],
    )

    print("IA:", response.choices[0].message.content)
