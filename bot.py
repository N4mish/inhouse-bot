import discord
from discord.ext import commands
import responses
import datetime
import asyncio
from inhousemanager import InhouseManager
import inhouse
from inhouse import Inhouse

# handles sending any message. called in run bot
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response != None:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

async def schedule_inhouse(client: commands.Bot, inhouse_manager: InhouseManager, time:datetime.datetime):
    now = datetime.datetime.now()
    wait_time = (time - now).total_seconds()
    await asyncio.sleep(wait_time)
    if time in inhouse_manager.timemap:
        await client.get_channel(1119693446890922016).send("Inhouse time!") 
        temp = inhouse_manager.timemap.pop(time)
        inhouse_manager.idmap.pop(temp.id)
    return

def run_discord_bot():
    TOKEN = 'MTExOTY5MTM5NTk2MDE0ODA1Mg.G5VYld.-zbXqtl7obHXTBA37Q-6jnnRb1enLhIMT0ErGo' # remove before commit 
    client = commands.Bot(command_prefix="?", intents=discord.Intents.all())
    inhouse_manager = InhouseManager()

    @client.event
    async def on_ready():
        synced = await client.tree.sync()
        print(synced)
        print(f"Slash commands synced - {str(len(synced))} commands synced")
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
    
    @client.tree.command(name='shutdown', description='Shuts down the bot.')
    async def shutdown(interaction: discord.Interaction):
        await interaction.response.send_message(content='Shutting down the bot.')
        await client.close()

    @client.tree.command(name='schedule', description='Schedules an inhouse message and reminders.')
    async def schedule(interaction: discord.Interaction):
        then = datetime.datetime.now().replace(hour=14, minute=51, second=30)
        await inhouse_manager.schedule(Inhouse("test", inhouse.InhouseBotType.INHOUSE, then))
        await interaction.response.send_message(content='Your inhouses have been scheduled!')
        await schedule_inhouse(client, inhouse_manager, then)

    @client.tree.command(name='test', description='test')
    async def test(interaction:discord.Interaction):
        await interaction.response.send_message(content=f'This is a test')
        
    @client.tree.command(name='cancel', description='Cancels an inhouse given an id.')
    async def cancel(interaction: discord.Interaction, id: str):
        await inhouse_manager.cancel(id)
        await interaction.response.send_message(content=f"Canceled inhouse with id {id}.")
    
    client.run(TOKEN)

    # scheduling. for future use, integrate this with database to find stored times based on server.