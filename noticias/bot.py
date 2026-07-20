import discord
from discord.ext import commands

from .armazenamento import NoticiasStorage
from .cog import NoticiasCog
from .config import NOTICIAS_POSTADAS_PATH
from .publicador import PublicadorNoticias
from .scraper import FlowGamesScraper


class NewsBot(commands.Bot):

    def __init__(self) -> None:
        intents = discord.Intents.default()
        super().__init__(intents=intents, command_prefix="$")

        self.publicador = PublicadorNoticias(
            scraper=FlowGamesScraper(),
            storage=NoticiasStorage(NOTICIAS_POSTADAS_PATH),
        )

    async def setup_hook(self) -> None:
        cog = NoticiasCog(self)
        await self.add_cog(cog)
        await self.tree.sync()
        cog.checar_noticias.start()

    async def on_ready(self) -> None:
        print(f"o bot {self.user} está pronto para varrer o Flow Games!")
