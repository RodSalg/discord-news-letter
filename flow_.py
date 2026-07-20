"""Script manual para checar rapidamente, via terminal, as notícias que o scraper encontra
(sem precisar subir o bot no Discord). A lógica de fato mora em noticias/scraper.py."""

import sys

from noticias.scraper import FlowGamesScraper

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    noticias = FlowGamesScraper().buscar_noticias()

    print(f"{len(noticias)} notícias encontradas:\n")
    for noticia in noticias:
        print(f"- [{noticia.categoria}] {noticia.titulo}")
        print(f"  Autor: {noticia.autor} | Data: {noticia.data}")
        print(f"  Link: {noticia.link}")
        print(f"  Imagem: {noticia.imagem}")
        print()


if __name__ == "__main__":
    main()
