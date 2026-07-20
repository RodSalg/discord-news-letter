import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

FLOW_GAMES_URL = "https://flowgames.gg"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
)

INTERVALO_MINUTOS = 30

NOTICIAS_POSTADAS_PATH = Path(__file__).resolve().parent.parent / "noticias_postadas.json"


def _ler_token() -> str:
    token = os.environ.get("TOKEN")
    if not token:
        raise RuntimeError("Defina TOKEN no arquivo .env com o token do bot do Discord.")
    return token


def _ler_canal_id() -> int:
    valor = os.environ.get("CANAL_NOTICIAS_ID")
    if not valor or not valor.isdigit():
        raise RuntimeError(
            "Defina CANAL_NOTICIAS_ID no arquivo .env com o ID numérico do canal onde as "
            "notícias devem ser postadas (ative o Modo Desenvolvedor no Discord e clique "
            "com o botão direito no canal -> Copiar ID)."
        )
    return int(valor)


TOKEN = _ler_token()
CANAL_NOTICIAS_ID = _ler_canal_id()
