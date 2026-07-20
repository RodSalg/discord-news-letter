import json
from pathlib import Path


class NoticiasStorage:

    def __init__(self, caminho: Path) -> None:
        self._caminho = caminho

    def carregar_links_postados(self) -> set[str]:
        if not self._caminho.exists():
            return set()
        with open(self._caminho, "r", encoding="utf-8") as f:
            return set(json.load(f))

    def marcar_como_postado(self, link: str) -> None:
        links = self.carregar_links_postados()
        links.add(link)
        with open(self._caminho, "w", encoding="utf-8") as f:
            json.dump(sorted(links), f, ensure_ascii=False, indent=2)
