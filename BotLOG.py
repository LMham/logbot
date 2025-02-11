import discord
from discord.ext import commands
from discord.ui import View, Button

TOKEN = "MTMzODQ5NTQ1Mjg0NDI2NTUzMg.GZb3yR.XkBKC-qXGbdokLHTGekZBXCrLuy5I2DMXHPVIc"  # ใส่โทเคนบอทที่นี่
GUILD_ID = 1338426711196565544  # ใส่ไอดีเซิร์ฟเวอร์ที่ต้องการให้ทำงาน
CHANNEL_ID = 1338496670375350403  # ใส่ไอดีช่องที่ต้องการให้บอทโพสต์ข้อความ
ALERT_CHANNEL_ID = 1338499987809505280  # ใส่ไอดีช่องที่ต้องการให้แจ้งเตือน
ALLOWED_USERS = {781749338664599562, 650343105387823104, 800495535655747634}  # ใส่ไอดีผู้ใช้ที่ได้รับอนุญาต

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
duty_users = set()

class DutyView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="เข้าเวร", style=discord.ButtonStyle.success)
    async def start_duty(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        if user.id not in ALLOWED_USERS:
            await interaction.response.send_message("คุณไม่ได้รับอนุญาตให้เข้าเวร!", ephemeral=True)
            return
        if user.id not in duty_users:
            duty_users.add(user.id)
            await interaction.response.send_message(f"🔵 {user.mention} กำลังเข้าเวร", ephemeral=True)
            await update_duty_status(interaction.guild)
        else:
            await interaction.response.send_message("คุณเข้าเวรอยู่แล้ว!", ephemeral=True)

    @discord.ui.button(label="ออกเวร", style=discord.ButtonStyle.danger)
    async def stop_duty(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        if user.id not in ALLOWED_USERS:
            await interaction.response.send_message("คุณไม่ได้รับอนุญาตให้ออกเวร!", ephemeral=True)
            return
        if user.id in duty_users:
            duty_users.remove(user.id)
            await interaction.response.send_message(f"⚫ {user.mention} ออกเวรแล้ว", ephemeral=True)
            await update_duty_status(interaction.guild)
            await send_alert(interaction.guild, user)
        else:
            await interaction.response.send_message("คุณยังไม่ได้เข้าเวร!", ephemeral=True)

async def update_duty_status(guild):
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        return
    await channel.purge(limit=5)  # ล้างข้อความเก่าก่อนโพสต์ใหม่
    
    view = DutyView()  # สร้างปุ่มใหม่
    if duty_users:
        mentions = "\n".join(f"🔵 <@{user_id}>" for user_id in duty_users)
        await channel.send(f"**รายชื่อผู้เข้าเวร:**\n{mentions}", view=view)
    else:
        await channel.send("ไม่มีใครเข้าเวรในขณะนี้", view=view)

async def send_alert(guild, user):
    alert_channel = bot.get_channel(ALERT_CHANNEL_ID)
    if alert_channel:
        await alert_channel.send(f"⚠️ {user.mention} ได้ออกเวรแล้ว!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    guild = bot.get_guild(GUILD_ID)
    if guild:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("บอทเข้าเวรพร้อมใช้งาน!", view=DutyView())

bot.run(TOKEN)
