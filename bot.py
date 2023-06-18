import discord
import responses

# handles sending any message. called in run bot
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'MTExOTY5MTM5NTk2MDE0ODA1Mg.GPVuNW.PJ9oinFqWrOfW010jA7_qapbuJH1pAXorugaHM' # remove before commit 
    client = discord.Client(intents=discord.Intents(messages=True, message_content=True)) # starts discord client for bot

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")

    @client.event
    async def on_message(message):
        # avoids bot responding to itself
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if len(user_message) > 0 and user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)
            
    client.run(TOKEN)