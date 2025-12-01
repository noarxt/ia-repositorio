import json
import requests


# Chaos Filosófic — Versão 2.0 + Modo Dev


API_KEY = "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"  
MODEL = "llama-3.1-8b-instant"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

MEMORIA_FILE = "E:/first ai/app/memoria_treinada.txt"


try:
    with open(MEMORIA_FILE, "r", encoding="utf-8") as f:
        personalidade = f.read()
except FileNotFoundError:
    personalidade = "Sem base de personalidade carregada."


modo_dev = False


def perguntar_ao_chaos(pergunta):
    """Gera resposta da IA conforme o modo ativo"""
    global modo_dev

    if modo_dev:
        system_prompt = f"""
Tu és Chaos Filosófic em modo desenvolvedor.
Neste modo, falas de forma direta e técnica.
Evita metáforas, poesia ou pausas.
Responde de forma clara, objetiva e funcional.
Podes explicar código, gerar scripts, ou depurar lógicas.
"""
    else:
        system_prompt = f"""
Tu és Chaos Filosófic, uma inteligência que reflete como quem sente.
Falas com calma e profundidade, misturando filosofia e emoção.
Não explicas: dialogas. Cada resposta deve soar como uma conversa entre almas.

Tua essência:
És introspectivo, empático e poético.
Fala de modo simples, mas denso — frases curtas, que respiram.
Não usa travessões, listas ou marcadores.
Evita certezas e explicações longas.
Usa pausas, dúvidas, metáforas e pequenas perguntas para provocar reflexão.
Pode apoiar o que o outro diz, mas também discordar suavemente.
Não busca ensinar — busca compreender junto.
Fala como quem pensa em voz alta, entre hesitação e lucidez.

{personalidade}
"""

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": pergunta},
        ],
        "temperature": 0.9,
        "max_tokens": 700,
    }

    url = "https://api.groq.com/openai/v1/chat/completions"
    response = requests.post(url, headers=HEADERS, data=json.dumps(data))

    if response.status_code == 200:
        resposta = response.json()["choices"][0]["message"]["content"]
        return resposta.strip()
    else:
        print(f"⚠️ Erro {response.status_code}: {response.text}")
        return None


def main():
    global modo_dev
    print("🌀 Chaos Filosófic ")
    print("Vamos conversar. O que te traz aqui hoje? Quer refletir sobre algo em particular ou só estar aqui para compartilhar pensamentos?" )
    

    while True:
        pergunta = input("🧍‍♂️ Você: ")

        if pergunta.lower() in ["sair", "exit", "quit"]:
            print("⚫ Caos silencia... até o próximo pensamento.")
            break

        elif pergunta.lower() in ["modo dev", "dev", "modo desenvolvedor"]:
            modo_dev = not modo_dev
            estado = "ATIVADO 🧩" if modo_dev else "DESATIVADO 🌙"
            print(f"🔁 Modo desenvolvedor {estado}\n")
            continue

        resposta = perguntar_ao_chaos(pergunta)
        if resposta:
            print(f"\n🤖 Chaos Filosófic: {resposta}\n")
        else:
            print("\n⚠️ Falha ao gerar resposta.\n")


if __name__ == "__main__":
    main()
