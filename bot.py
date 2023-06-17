import discord
import responses

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTExOTY5MTM5NTk2MDE0ODA1Mg.G2Hh1t.BtHRP899r8y7tjlk5ABEjyq1Or1T7jTjwqWbv8'
    client = discord.Client(intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        print(user_message)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
            
    client.run(TOKEN)