![2](https://repository-images.githubusercontent.com/1096099312/03ae624f-f171-4de1-8abf-0758b6865b4f)

# Plex Discord Rich Presence Bot

Small Discord bot that sets its own Rich Presence based on what a Plex user is
currently watching. Designed for setups where you want a Discord account to
show the movie or TV episode playing on your Plex server (e.g. a “KeeCinema”-style
cinema account).

## Pull from DockerHub

[![Docker Pulls](https://img.shields.io/docker/pulls/keenaanee/discord-plex-drpp)](https://hub.docker.com/r/keenaanee/discord-plex-drpp)

## What it does

- Connects to your Plex server via URL and token.
- Watches active Plex sessions and optionally filters to a single Plex username.
- Updates the Discord bot’s Rich Presence with:
  - Movie title and year, or
  - TV show name, season/episode code, and episode title.
- Shows play/pause status (via the small icon and text).
- Optionally includes timestamps so Discord shows the remaining time.
- Runs as a simple, lightweight polling bot inside Docker.

## Requirements

- A Plex server you can reach from the container (URL + token).
- A Discord bot with:
  - No special intents required (it only updates its own presence).
- Docker (Unraid, Linux, etc.) or plain Python if you prefer running without Docker.

## Configuration (environment variables)

All configuration is done via environment variables:

- `PLEX_URL` (required)  
  Your Plex server URL, including port.  
  Example: `http://192.168.x.x:32400`

- `PLEX_TOKEN` (required)  
  Your Plex API token.

- `BOT_TOKEN` (required)  
  Discord bot token for this Rich Presence bot.

- `TARGET_USER` (optional)  
  Plex username to track. If set, the bot only uses sessions from this user.  
  If left empty, it will fall back to “any active session”.

You can use an `.env` file or pass these directly as `-e` flags.

## Running with Docker

### Build

```bash
docker build -t your-docker-user/plex-discord-bot .

Run

docker run -d \
  --name plex-discord-bot \
  -e PLEX_URL="http://192.168.x.x:32400" \
  -e PLEX_TOKEN="your-plex-token" \
  -e BOT_TOKEN="your-discord-bot-token" \
  -e TARGET_USER="YourPlexUsername" \
  --restart unless-stopped \

  your-docker-user/plex-discord-bot

