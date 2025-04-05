from threading import Thread
from keep_alive import keep_alive
from discord.ext import commands
from datetime import timedelta
import os
import discord
from dotenv import load_dotenv
import json

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

def load_data():
    try:
        with open('data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'moderators_roles': [], 'whitelist': [], 'owners': [], 'infractions': {}}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

data = load_data()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="-", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")
    print(f"Commandes chargées: {list(bot.commands)}")
    await bot.tree.sync()

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if before.timed_out_until != after.timed_out_until:
        if after.timed_out_until is not None:
            log_channel = discord.utils.get(after.guild.text_channels, name="logs")
            if log_channel:
                await log_channel.send(f"{after.mention} a été mis en timeout jusqu'à {after.timed_out_until}.")

@bot.event
async def on_message(message):
    if message.author.bot or message.author.id in data['whitelist']:
        return

    forbidden_words = ["connard", "pute", "chienne", "salope", "stupide", "tdc", "tdbl", "slp", "jte bz", "ferme ta gueule", 
              "fils de pute", "negre", "negro", "negrion", "negresse", "negrre", "enculé", "fdp", "trou du cul", 
              "viole", "violeur", "vi0l", "viol", "violeuse", "violer", "pd", "sale pd"]

    if any(word in message.content.lower() for word in forbidden_words):
        try:
            await message.delete()
        except discord.NotFound:
            print("Message déjà supprimé.")
        except discord.Forbidden:
            print("Permissions insuffisantes pour supprimer le message.")
        except discord.HTTPException:
            print("Erreur lors de la suppression du message.")

        user_id = str(message.author.id)
        data['infractions'][user_id] = data['infractions'].get(user_id, 0) + 1
        save_data(data)

        if data['infractions'][user_id] == 1:
            await message.channel.send(f"{message.author.mention}, ⚠️ Attention! Utilisation de langage inapproprié.")
        elif data['infractions'][user_id] == 2:
            await message.channel.send(f"{message.author.mention}, ⚠️ Dernier avertissement!")
        elif data['infractions'][user_id] >= 3:
            try:
                await message.author.timeout(timedelta(minutes=15))
                await message.channel.send(f"{message.author.mention} a été mis(e) en timeout pour 15 minutes.")
                del data['infractions'][user_id]
                save_data(data)
            except discord.Forbidden:
                await message.channel.send("Je n'ai pas la permission de timeout cet utilisateur.")
            except discord.HTTPException:
                await message.channel.send("Une erreur s'est produite lors du timeout.")

    await bot.process_commands(message)

@bot.command()
async def aide(ctx):
    embed = discord.Embed(title="Commandes disponibles", color=discord.Color.blue())
    embed.add_field(name="-wl @user", value="Ajoute un utilisateur à la whitelist.", inline=False)
    embed.add_field(name="-unwl @user", value="Retire un utilisateur de la whitelist.", inline=False)
    embed.add_field(name="-owner @user", value="Ajoute un utilisateur en tant qu'owner.", inline=False)
    embed.add_field(name="-unowner @user", value="Retire un utilisateur des owners.", inline=False)
    await ctx.send(embed=embed)

def start_flask():
    print("🌐 Démarrage de Flask (keep_alive)")
    keep_alive()

def start_bot():
    print("🤖 Démarrage du bot Discord")
    try:
        bot.run(token)
    except Exception as e:
        print(f"❌ Erreur au lancement du bot : {e}")

def start():
    print("🚀 Script lancé")
    flask_thread = Thread(target=start_flask)
    flask_thread.start()

    start_bot()

if __name__ == "__main__":
    start()