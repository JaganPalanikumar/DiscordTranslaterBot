import responses
import discord

async def send_message(message, user_message, is_private):
    try:
        response = responses.translate(user_message)
        await message.reply(response)

    except Exception as e:
        print(e)


def run_discord_bot(): 
    secretToken = "YOUR DISCORD BOT API TOKEN HERE"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        await send_message(message, str(message.content), is_private=False)

    client.run(secretToken)