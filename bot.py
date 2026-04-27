import responses
import discord
import os
from discord import app_commands


# Load key=value pairs from a local .env file into environment variables.
def load_env_file(file_path=".env"):
    if not os.path.exists(file_path):
        return

    with open(file_path, "r", encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip())


# Initialize Discord client settings, register events, and start the bot session.
def run_discord_bot(): 
    load_env_file()
    secretToken = os.getenv("DISCORD_BOT_TOKEN")
    guild_id = os.getenv("DISCORD_GUILD_ID")

    if not secretToken:
        raise ValueError("DISCORD_BOT_TOKEN is missing. Add it to your .env file.")

    #TODO - 1 (Setting up Bot)
    intents = discord.Intents.default() #define default set of discord events bot can listen to
    intents.message_content = True #lets bot read text content of messages (not inculded default)
    client = discord.Client(intents=intents) #creates client (bot object that connects to discord), tells it which events it can recieve
    tree = app_commands.CommandTree(client) #slash command manager, helps define slash commands

    @tree.command(name="thelp", description="Show translation bot help.")
    async def thelp_command(interaction: discord.Interaction):
        await interaction.response.send_message(responses.translate("/thelp"))

    @tree.command(name="tlangs", description="List available translation languages.")
    async def tlangs_command(interaction: discord.Interaction):
        await interaction.response.send_message(responses.translate("/tlangs"))

    @tree.command(name="translate", description="Translate text to a target language.")
    @app_commands.describe(text="Text to translate", language="Target language (optional)")
    #TODO - 2 (Translate Slash Command)
    async def translate_command(
        interaction: discord.Interaction,
        text: str,
        language: str | None = None,
    ):
        command_text = f"/t {text}" if not language else f"/t {text} - {language}"
        await interaction.response.send_message(responses.translate(command_text))

    @client.event
    # Announce in console when the bot account has connected and is ready.
    async def on_ready():
        try:
            if guild_id:
                await tree.sync(guild=discord.Object(id=int(guild_id)))
                print(f"Slash commands synced to guild {guild_id}.")
            else:
                await tree.sync()
                print("Slash commands synced globally.")
        except Exception as e:
            print(f"Slash command sync failed: {e}")

        print(f'{client.user} is now running!')

    # TODO - 3 (Handle every new message, ignoring the bot's own messages to prevent loops.)
    @client.event #registers function as a discord event handler 
    async def on_message(message): #built in discord event name
        if message.author == client.user: #if the message was sent by the bot, ignore
            return

        try: #try to call translate function, if not raise error
            response = responses.translate(str(message.content))
            await message.reply(response)
        except Exception as e:
            print(e)

    client.run(secretToken) #TODO - 4 (runs bot using secret token)
