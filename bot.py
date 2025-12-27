import os
import discord
from memory import add, get
from ai_router import ask_all, SYSTEM_PROMPT

TOKEN = os.getenv("DISCORD_TOKEN")
CODE_CHANNEL_ID = int(os.getenv("CODE_CHANNEL_ID"))

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

ALLOWED_EXT = (
    ".py", ".js", ".ts", ".java", ".cpp", ".c",
    ".html", ".css", ".json", ".md", ".txt"
)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != CODE_CHANNEL_ID:
        return

    text = message.content.strip()
    file_text = ""

    if message.attachments:
        att = message.attachments[0]
        if att.filename.lower().endswith(ALLOWED_EXT) and att.size < 100_000:
            raw = await att.read()
            file_text = raw.decode("utf-8", errors="ignore")

    if not text and not file_text:
        return

    async with message.channel.typing():
        add(message.channel.id, "user", text)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get(message.channel.id))

        if file_text:
            messages.append({
                "role": "user",
                "content": f"Attached file:\n{file_text}"
            })

        reply = await ask_all(messages)

        add(message.channel.id, "assistant", reply)
        await message.channel.send(reply[:2000])

client.run(TOKEN)
