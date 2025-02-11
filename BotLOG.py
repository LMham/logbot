import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN")  # ดึงค่า Token จาก GitHub Secrets

if TOKEN is None:
    raise ValueError("Token ไม่สามารถเข้าถึงได้! กรุณาตรวจสอบ GitHub Secrets")  # หากไม่ได้ Token จะเกิดข้อผิดพลาด

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"บอทกำลังออนไลน์แล้ว: {bot.user}")


bot.run(TOKEN)
