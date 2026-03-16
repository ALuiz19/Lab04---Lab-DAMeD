# sem_acesso.py
import json
from pathlib import Path

import requests


BASE_DIR = Path(__file__).resolve().parent


def ler_configuracao(origem: str):
    if origem == "local":
        with open(BASE_DIR / "config.json", encoding="utf-8") as f:
            return json.load(f)
    elif origem == "http":
        resp = requests.get("http://config-srv/config")
        return resp.json()
    elif origem == "s3":
        raise NotImplementedError("S3 não configurado neste lab")

try:
    cfg = ler_configuracao("local")
    print("Configuração carregada:", cfg)
except FileNotFoundError:
    print("config.json não encontrado — crie um para testar")