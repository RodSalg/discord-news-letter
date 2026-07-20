import asyncio
from dataclasses import replace

import requests

from .armazenamento import NoticiasStorage
from .modelos import Noticia
from .scraper import FlowGamesScraper


class PublicadorNoticias:
    """Busca notícias novas no Flow Games e controla quais já foram postadas."""

    def __init__(self, scraper: FlowGamesScraper, storage: NoticiasStorage) -> None:
        self._scraper = scraper
        self._storage = storage

    async def buscar_novas(self) -> list[Noticia]:
        noticias = await asyncio.to_thread(self._scraper.buscar_noticias)
        links_postados = self._storage.carregar_links_postados()
        novas = [noticia for noticia in noticias if noticia.link not in links_postados]
        novas.reverse()  # da mais antiga pra mais nova, pra manter ordem cronológica no canal

        return await asyncio.gather(*(self._com_resumo(noticia) for noticia in novas))

    async def _com_resumo(self, noticia: Noticia) -> Noticia:
        try:
            resumo = await asyncio.to_thread(self._scraper.buscar_resumo, noticia.link)
        except requests.RequestException:
            return noticia
        return replace(noticia, resumo=resumo)

    def marcar_como_postada(self, noticia: Noticia) -> None:
        self._storage.marcar_como_postado(noticia.link)
