from dataclasses import dataclass


@dataclass(frozen=True)
class Noticia:
    titulo: str
    link: str
    categoria: str | None
    autor: str | None
    data: str | None
    imagem: str | None
    resumo: str | None = None
