import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # 注意！要開這個才能收到訊息內容

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot 上線了！目前登入為：{bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return  # 不要回自己或其他 bot

    await message.channel.send(f"{message.content}"*6)
    await message.channel.send("這是我加碼回的一句話。")

bot.run(TOKEN)