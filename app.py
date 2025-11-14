import os
import time

import discord
from discord import Activity, ActivityType
from discord.ext import tasks
from plexapi.server import PlexServer

PLEX_URL = os.getenv("PLEX_URL")
PLEX_TOKEN = os.getenv("PLEX_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")
TARGET_USER = os.getenv("TARGET_USER", "KeeCinema")

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

client = discord.Client(intents=discord.Intents.none())


@client.event
async def on_ready():
    print("Bot is ready, starting poll loop")
    poll.start()


@tasks.loop(seconds=30)
async def poll():
    try:
        sessions = plex.sessions()
    except Exception as e:
        print(f"Error getting sessions from Plex: {e}")
        await client.change_presence(activity=None)
        return

    for session in sessions:
        user = None

        # Try to get the username from different possible locations
        if hasattr(session, "user") and session.user and hasattr(session.user, "title"):
            user = session.user.title
        elif hasattr(session, "usernames") and session.usernames:
            user = session.usernames[0]

        # Match specific target user or fallback to "any" if we can't detect
        if user == TARGET_USER or user is None:
            player_state = (
                getattr(session.player, "state", "playing")
                if hasattr(session, "player")
                else "playing"
            )
            paused = player_state != "playing"

            # Build title/lines based on media type
            if session.type == "movie":
                year = f" ({session.year})" if getattr(session, "year", None) else ""
                details = f"{session.title}{year}"
                main_line = details
                state_text = "Movie"
                large = "movie"

            elif session.type == "episode":
                show = getattr(session, "grandparentTitle", "Unknown Show")
                season = (
                    f"S{session.parentIndex:02d}"
                    if getattr(session, "parentIndex", None)
                    else ""
                )
                ep = (
                    f"E{session.index:02d}"
                    if getattr(session, "index", None)
                    else ""
                )
                details = f"{show} - {season}{ep}: {session.title}".lstrip(" -")
                main_line = show
                state_text = f"{season}{ep}: {session.title}".lstrip(": ")
                large = "tv"

            else:
                details = getattr(session, "title", "Media")
                main_line = details
                state_text = session.type.capitalize()
                large = "plex"

            # Timestamps for elapsed/remaining
            timestamps = None
            if (
                not paused
                and getattr(session, "viewOffset", None) is not None
                and getattr(session, "duration", None) is not None
            ):
                elapsed = session.viewOffset / 1000
                duration = session.duration / 1000
                start = int(time.time() - elapsed)
                end = int(start + duration)
                timestamps = {"start": start, "end": end}

            activity = Activity(
                type=ActivityType.watching,
                name=main_line,  # main visible line (movie/show title or show name)
                details=details,
                state=state_text,
                large_image=large,
                large_text="Watching on Plex",
                small_image="paused" if paused else "playing",
                small_text=player_state.capitalize(),
                timestamps=timestamps,
            )

            await client.change_presence(activity=activity)
            return

    # No matching/active sessions
    await client.change_presence(activity=None)


client.run(BOT_TOKEN)
