import discord
import os
from dotenv import load_dotenv
import google.generativeai as genai

# config files
from prompt_config import topic_prompts, user_topic

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

intents = discord.Intents.default()
intents.message_content = True  # 注意！要開這個才能收到訊息內容

bot = discord.Bot(intents=intents, sync_commands=True)

# 初始化 Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

@bot.event
async def on_ready():
    print(f"✅ Bot 上線了！目前登入為：{bot.user}")

@bot.slash_command(name="chat", description="用 Gemini AI 回答你的提問")
async def chat(ctx, prompt: str = None, topic: str = None):
    await ctx.defer()  # 預防 timeout

    user_id = ctx.author.id
    if topic:
        if topic not in topic_prompts:
            await ctx.respond(f"⚠️ 不支援的語氣：{topic}，目前支援：{list(topic_prompts.keys())}")
            return
        user_topic[user_id] = topic
        if prompt is None:
            await ctx.respond(f"✅ 語氣設定為：{topic}，你可以輸入問題開始聊天")
            return
    
    if prompt is None:
        await ctx.respond("❗ 請輸入你的問題或提示。")
        return

    topic_prefix = topic_prompts.get(user_topic.get(user_id, "默認"), "")
    full_prompt = f"{topic_prefix}User: {prompt}\nAI:"

    
    try:
        response = model.generate_content(full_prompt)
        reply = response.text
        await ctx.respond(reply)
    except Exception as e:
        await ctx.respond("❌ AI 回答失敗：" + str(e))

@bot.slash_command(name="lan_detect", description="測試目前用戶的語氣設定")
async def lan_detect(ctx):
    await ctx.defer()  # 預防 timeout

    user_id = ctx.author.id
    current_topic = user_topic.get(user_id, "默認")
    await ctx.respond(f"🔍 目前語氣設定為：{current_topic}")

@bot.slash_command(name="ping", description="測試機器人是否在線")
async def ping(ctx):
    await ctx.defer()  # 預防 timeout

    await ctx.respond("🏓 Pong! 機器人在線！")

bot.run(TOKEN)