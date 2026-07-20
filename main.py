from noticias.bot import NewsBot
from noticias.config import TOKEN


def main() -> None:
    bot = NewsBot()
    bot.run(token=TOKEN)


if __name__ == "__main__":
    main()
