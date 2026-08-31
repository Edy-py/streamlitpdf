import json
import os

ARQUIVO_CATALOGO = "catalogo_servicos.json"
ARQUIVO_HISTORICO = "historico_servicos.json"

def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def salvar_json(dados, caminho):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)