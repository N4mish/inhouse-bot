import discord
from discord.ext import commands
import responses
import datetime
import asyncio
from inhousemanager import InhouseManager
from inhouse import Inhouse, InhouseBotType
from dateutil import parser
from dateutil.tz import gettz
# handles sending any message. called in run bot

class InterestCheck(discord.ui.View):
    def __init__(self, inhouse: Inhouse):
        super().__init__()
        self.inhouse = inhouse
    @discord.ui.button(label="Yes!", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction, button):
        if interaction.user not in self.inhouse.participants:
            await interaction.response.send_message("You've been added to the inhouse list!", ephemeral=True)
            await interaction.user.send("You have been added to the inhouse at a time!")
            self.inhouse.participants.append(interaction.user)
        else:
            await interaction.response.send_message("You're already in the inhouse list!")
        print(self.inhouse.participants)
        


async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        if response != None:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

async def schedule_inhouse(client: commands.Bot, inhouse_manager: InhouseManager, time:datetime.datetime):
    now = datetime.datetime.now()
    now = now.replace(tzinfo=gettz("America/Chicago"))
    print(f"now: {now} then: {time}")
    wait_time = (time - now).total_seconds()
    await asyncio.sleep(wait_time)

    # activating the inhouse
    if time in inhouse_manager.timemap:
        inhouse = inhouse_manager.timemap[time]
        channel = 1119693446890922016
        if inhouse.type == InhouseBotType.IC:
            await client.get_channel(channel).send(f"Interest check! Please react to this message if you'd like to play inhouse {inhouse.id} on this date!", view=InterestCheck(inhouse))
        elif inhouse.type == InhouseBotType.INHOUSE:
            await client.get_channel(channel).send(f"Inhouse time! Inhouse {inhouse.id} is ready!") 
        else:
            # should never happen
            raise Exception("Inhouse type error.")
        temp = inhouse_manager.timemap.pop(time)
        inhouse_manager.idmap.pop(temp.id)
    else:
        await client.get_channel(channel).send("That inhouse was canceled. :(") 
    return

def run_discord_bot():
    TOKEN = 'MTExOTY5MTM5NTk2MDE0ODA1Mg.G5VYld.-zbXqtl7obHXTBA37Q-6jnnRb1enLhIMT0ErGo' # remove before commit 
    client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
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

        # if len(user_message) > 0 and user_message[0] == '?':
        #     user_message = user_message[1:]
        #     await send_message(message, user_message, is_private=True)
        # else:
        #     await send_message(message, user_message, is_private=False)
    
    @client.tree.command(name='shutdown', description='Shuts down the bot.')
    async def shutdown(interaction: discord.Interaction):
        await interaction.response.send_message(content='Shutting down the bot.')
        await client.close()

    # Please specify date and time in the following format: M/DD/YYYY HH:MM:SS Timezone (in 24h time)
    @client.tree.command(name='schedule', description='Schedules an inhouse message and reminders.')
    async def schedule(interaction: discord.Interaction, type: InhouseBotType, id: str, time: str):
        try:
            print(time)
            if time.lower().strip() == 'now':
                then = datetime.datetime.now().replace(tzinfo=gettz("America/Chicago"))
            else:
                then = parser.parse(time, tzinfos={"CST": gettz("America/Chicago"), "CDT": gettz("America/Chicago")})
        except:
            await interaction.response.send_message(content=f"Could not schedule inhouse. Time in invalid format. Please specify date and time in the following format: M/DD/YYYY HH:MM:SS Timezone (in 24h time)")
            return
        await inhouse_manager.schedule(Inhouse(id, type, then))
        await interaction.response.send_message(content='Your inhouses have been scheduled!')
        await schedule_inhouse(client, inhouse_manager, then)
        
    @client.tree.command(name='cancel', description='Cancels an inhouse given an id.')
    async def cancel(interaction: discord.Interaction, id: str):
        id = id.strip()
        res = await inhouse_manager.cancel(id)
        if res:
            await interaction.response.send_message(content=f"Canceled inhouse with id {id}.")
        else:
            await interaction.response.send_message(content=f"Inhouse with id {id} does not exist or an error occurred.")
    
    
    client.run(TOKEN)

    # scheduling. for future use, integrate this with database to find stored times based on server.