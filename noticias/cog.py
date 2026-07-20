from typing import TYPE_CHECKING

import discord
from discord import Interaction, app_commands
from discord.ext import commands, tasks

from .config import CANAL_NOTICIAS_ID, INTERVALO_MINUTOS
from .modelos import Noticia

if TYPE_CHECKING:
    from .bot import NewsBot


class NoticiasCog(commands.Cog):

    def __init__(self, bot: "NewsBot") -> None:
        self.bot = bot

    async def cog_unload(self) -> None:
        self.checar_noticias.cancel()

    @tasks.loop(minutes=INTERVALO_MINUTOS)
    async def checar_noticias(self) -> None:
        await self._publicar_novas()

    @checar_noticias.before_loop
    async def _antes_de_checar(self) -> None:
        await self.bot.wait_until_ready()

    async def _obter_canal(self) -> discord.abc.Messageable | None:
        canal = self.bot.get_channel(CANAL_NOTICIAS_ID) or await self.bot.fetch_channel(CANAL_NOTICIAS_ID)
        if not isinstance(canal, discord.abc.Messageable):
            print(f"Canal {CANAL_NOTICIAS_ID} não encontrado ou não aceita mensagens.")
            return None
        return canal

    async def _publicar_novas(self) -> list[Noticia]:
        canal = await self._obter_canal()
        if canal is None:
            return []

        novas = await self.bot.publicador.buscar_novas()
        for noticia in novas:
            await canal.send(
                content="@everyone",
                embed=self._montar_embed(noticia),
                allowed_mentions=discord.AllowedMentions(everyone=True),
            )
            self.bot.publicador.marcar_como_postada(noticia)

        return novas

    @app_commands.command(name="refresh", description="Varre o Flow Games agora e posta as notícias novas no canal")
    async def refresh(self, interaction: Interaction) -> None:
        await interaction.response.defer(ephemeral=True)
        novas = await self._publicar_novas()

        if not novas:
            await interaction.followup.send("Nenhuma notícia nova encontrada.")
            return

        await interaction.followup.send(f"{len(novas)} notícia(s) nova(s) publicada(s) no canal.")

    def _montar_embed(self, noticia: Noticia) -> discord.Embed:
        embed = discord.Embed(
            title=noticia.titulo,
            url=noticia.link,
            description=noticia.resumo,
            color=discord.Color.blurple(),
        )

        if noticia.categoria:
            embed.set_author(name=noticia.categoria)

        rodape = [parte for parte in (f"Por {noticia.autor}" if noticia.autor else None, noticia.data) if parte]
        if rodape:
            embed.set_footer(text=" • ".join(rodape))

        if noticia.imagem:
            embed.set_image(url=noticia.imagem)

        return embed
