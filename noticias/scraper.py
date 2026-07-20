import requests
from bs4 import BeautifulSoup
from bs4.element import Tag

from .config import FLOW_GAMES_URL, USER_AGENT
from .modelos import Noticia


class FlowGamesScraper:

    def __init__(self, url: str = FLOW_GAMES_URL, user_agent: str = USER_AGENT) -> None:
        self._url = url
        self._headers = {"User-Agent": user_agent}

    def buscar_noticias(self) -> list[Noticia]:
        resposta = requests.get(self._url, headers=self._headers, timeout=15)
        resposta.raise_for_status()
        return self._extrair(resposta.text)

    def buscar_resumo(self, link: str) -> str | None:
        """Pega o resumo editorial da matéria (meta description) direto da página do artigo."""
        resposta = requests.get(link, headers=self._headers, timeout=15)
        resposta.raise_for_status()

        soup = BeautifulSoup(resposta.text, "html.parser")
        meta = soup.select_one('meta[property="og:description"]') or soup.select_one('meta[name="description"]')
        if not meta:
            return None

        conteudo = meta.get("content")
        return str(conteudo).strip() if conteudo else None

    def _extrair(self, html: str) -> list[Noticia]:
        soup = BeautifulSoup(html, "html.parser")
        noticias: list[Noticia] = []

        for item in soup.select("ul.list-post > li"):
            link_tag = item.select_one("div.content h3 a") or item.select_one("div.content h2 a")
            if not link_tag:
                continue

            link = link_tag.get("href")
            if not link:
                continue

            categoria_tag = item.select_one("div.content a.tag")
            autor_tag = item.select_one("span.author a")
            data_tag = item.select_one("span.data")
            imagem = self._resolver_imagem(item)

            noticias.append(
                Noticia(
                    titulo=link_tag.get_text(strip=True),
                    link=str(link),
                    categoria=categoria_tag.get_text(strip=True) if categoria_tag else None,
                    autor=autor_tag.get_text(strip=True) if autor_tag else None,
                    data=data_tag.get_text(strip=True) if data_tag else None,
                    imagem=imagem,
                )
            )

        return noticias

    def _resolver_imagem(self, item: Tag) -> str | None:
        img_tag = item.select_one("div.thumb img")
        if not img_tag:
            return None

        src = img_tag.get("src")
        if not src:
            return None

        src = str(src)
        return f"{self._url}{src}" if src.startswith("/") else src
