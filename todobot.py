import discord
from discord import Option
import os
import google.generativeai as genai
from dotenv import load_dotenv
from myTool import get_prompt_for_todo, extract_json_from_text

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

@bot.event
async def on_ready():
    print(f"✅ Bot 上線了！目前登入為：{bot.user}")

# Slash command
@bot.slash_command(name="todo", description="分析自然語言句子中的事件與時間")
async def todo(
    ctx: discord.ApplicationContext,
    sentence: str = Option(description="輸入一般的句子就好，例如：明天交線性代數作業、下禮拜日打麻將")
):
    await ctx.defer()
    prompt = get_prompt_for_todo(sentence)
    try:
        result = model.generate_content(prompt).text
        parsed = extract_json_from_text(result)
        await ctx.respond(f"✅ 分析結果：\n```json\n{parsed}\n```")
    except Exception as e:
        await ctx.respond(f"❌ 發生錯誤：{e}")

bot.run(DISCORD_TOKEN)