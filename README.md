# discord-news-letter

Discord bot that scrapes [flowgames.gg](https://flowgames.gg) and posts new articles to a
dedicated channel, with an `@everyone` mention and a short summary pulled from each article.

## Features

- Scrapes the Flow Games homepage for the latest articles (title, category, author, date, image).
- Fetches a short summary (the article's own meta description) for every new article.
- Keeps track of already-posted links in `noticias_postadas.json`, so nothing gets posted twice,
  even across restarts.
- Checks for new articles automatically every 30 minutes.
- `/refresh` slash command to trigger a check on demand.

## Project structure

```
main.py                    # entry point
noticias/
  config.py                 # env vars, constants, paths
  modelos.py                 # Noticia dataclass
  scraper.py                 # FlowGamesScraper: HTML scraping
  armazenamento.py           # NoticiasStorage: posted-links persistence
  publicador.py              # PublicadorNoticias: new-article selection + summaries
  cog.py                     # NoticiasCog: scheduled loop + /refresh command
  bot.py                     # NewsBot: discord.py bot wiring
flow_.py                    # manual CLI check (prints scraped articles, no Discord needed)
```

## Setup

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

Create a `.env` file in the project root:

```
TOKEN=your-discord-bot-token
CANAL_NOTICIAS_ID=the-numeric-channel-id
```

To get the channel ID: enable Developer Mode in Discord (Settings > Advanced), then right-click
the channel and choose "Copy ID" (or copy the channel link — the ID is the last number in the URL).

The bot needs the **Mention @everyone, @here, and All Roles** permission in that channel for the
`@everyone` ping to actually notify anyone.

## Running

```bash
uv run python main.py
```

## Manual scrape check

To see what the scraper finds without starting the bot:

```bash
uv run python flow_.py
```
