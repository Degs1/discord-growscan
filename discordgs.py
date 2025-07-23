from discord import app_commands
import discord

token="token dc"
tokenapi="api token"
BOT_CHANNEL=1397502885373415424

isRunning=False

from discord.ext import commands
import asyncio
import aiohttp

# --- SETUP DASAR BOT ---
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_data(url):
    timeout = aiohttp.ClientTimeout(total=10)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                # Jika server sudah kirim JSON dengan format {status, message}
                return await response.json()
    except aiohttp.ClientConnectorError:
        return { "status": False, "message": "🔌 Gagal nyambung ke server" }
    except asyncio.TimeoutError:
        return { "status": False, "message": "⏱️ Timeout! Server terlalu lama merespon" }
    except aiohttp.ClientError as e:
        print(f"{type(e).__name__} - {e}")
        return { "status": False, "message": f"⚠️ Client error: " }
    except Exception as e:
        print(f"{type(e).__name__} - {e}")
        return { "status": False, "message": f"❌ Error: " }
        
def format_item_response(response, world):
    if not isinstance(response, list):
        return {
            "status": False,
            "message": "Format data salah, seharusnya list."
        }

    floating = ""
    world_item = ""

    for item in response:
        line = f"<a:arrow:1397515385313562744> {item['name']} : {item['count']}\n"
        if item["tipe"] == "object":
            floating += line
        elif item["tipe"] == "block":
            world_item += line

    message = f"""**Result from {world}**

**- Floating Item :**
{floating}

**<:wldegs:1397515288714678333> World Item :**
{world_item}"""

    return {
        "status": True,
        "message": message
    }
        
@bot.tree.command(name="degsgs", description="Scanner For your world :v")
@app_commands.describe(world="enter your world name")
async def fetch_data_command(interaction: discord.Interaction, world: str):
    await interaction.response.defer(ephemeral=True, thinking=True)
    if interaction.channel.id != BOT_CHANNEL:
        print("not a bot channel")
        return await interaction.edit_original_response(content=f"Please use this command in <#{BOT_CHANNEL}>")
    
    global isRunning
    if not isRunning:
        isRunning = True
        if " " in world or not world.isalnum():
            isRunning = False
            return await interaction.edit_original_response(content=f"**{world}**. your world is invalid please recheck!")
        
        # await asyncio.sleep(4)
        await interaction.edit_original_response(content=f"warping to **{world}** please wait.")
        respon = await fetch_data(f"http://45.115.224.103:5000/bot/degsgs?world={world}&token={tokenapi}")
        isRunning = False
        if isinstance(respon,dict) and "status" in respon:
            await interaction.edit_original_response(content=respon["message"])
        elif isinstance(respon,list):
            result=format_item_response(respon,world)
            await interaction.edit_original_response(content=result["message"])
            	
    else:
        return await interaction.edit_original_response(content="Too many people use please wait!")
    
    isRunning = False
    	
    
@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, 
            name="/degsgs"
        ),status=discord.Status.idle)
    print(f'Bot telah login sebagai {bot.user}')
    
@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error pada event {event}: {args} {kwargs}')
 
@bot.event
async def on_message(msg):
	print(f"[MSG] From {msg.author} : {msg.content}")

bot.run(token)
