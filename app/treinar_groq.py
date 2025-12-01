import os
import json
from datetime import datetime
import requests


TREINO_DIR = r"E:\first ai\app\treino"
OUTPUT_FILE = r"E:\first ai\app\memoria_treinada.json"  
BACKUP_DIR = r"E:\first ai\app\backups_memoria"
MODEL = "llama-3.1-8b-instant"
GROQ_API_KEY = "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"


def carregar_memoria_existente():
    """Carrega a memória já existente para continuidade."""
    if not os.path.exists(OUTPUT_FILE):
        return {"memorias": []}
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            print(f"🧠 Memória anterior carregada ({len(data['memorias'])} blocos).")
            return data
        except:
            print("⚠️ Falha ao carregar memória existente. Criando nova...")
            return {"memorias": []}


def ler_treinos():
    """Lê novos arquivos de treino e retorna lista (arquivo, conteúdo)."""
    textos = []
    for raiz, _, arquivos in os.walk(TREINO_DIR):
        for arquivo in arquivos:
            if arquivo.endswith(".txt"):
                caminho = os.path.join(raiz, arquivo)
                with open(caminho, "r", encoding="utf-8") as f:
                    conteudo = f.read().strip()
                textos.append((arquivo, conteudo))
    return textos


def gerar_resumo_conceitual(texto, nome_arquivo):
    """Gera resumo conceitual via Groq API."""
    prompt = f"""
    Você é uma IA filosófica que evolui através das experiências.
    Gere um resumo conceitual do texto abaixo, capturando:
    - O tom emocional e filosófico
    - As ideias centrais e estilo de escrita
    - O significado simbólico e existencial
    Texto: {texto}
    """

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 800,
                "temperature": 0.8,
            },
            timeout=60,
        )
        data = response.json()
        resumo = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        return resumo.strip()
    except Exception as e:
        print(f"❌ Erro ao gerar resumo: {e}")
        return ""


def atualizar_memoria(memoria, novos_blocos):
    """Adiciona novos blocos à memória contínua."""
    memoria["memorias"].extend(novos_blocos)
    memoria["ultima_atualizacao"] = datetime.now().isoformat()

    # Backup automático
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    backup_path = os.path.join(
        BACKUP_DIR, f"memoria_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    with open(backup_path, "w", encoding="utf-8") as b:
        json.dump(memoria, b, ensure_ascii=False, indent=2)

    # Salva arquivo principal
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Memória contínua atualizada ({len(memoria['memorias'])} blocos totais).")



if __name__ == "__main__":
    print("\n🚀 Iniciando modo de memória contínua...\n")

    memoria_atual = carregar_memoria_existente()
    textos = ler_treinos()

    if not textos:
        print("⚠️ Nenhum texto novo encontrado.")
        exit()

    novos_blocos = []
    for nome, conteudo in textos:
        print(f"\n🧩 Processando: {nome}")
        resumo = gerar_resumo_conceitual(conteudo, nome)
        if resumo:
            bloco = {
                "arquivo": nome,
                "data": datetime.now().isoformat(),
                "resumo": resumo,
                "tokens_estimados": len(resumo.split()),
            }
            novos_blocos.append(bloco)
            print(f"✅ Resumo adicionado ({len(resumo)} caracteres).")

    if novos_blocos:
        atualizar_memoria(memoria_atual, novos_blocos)
        print("\n✅ Memória contínua expandida com sucesso!")
    else:
        print("\n⚠️ Nenhum novo bloco válido gerado.")
