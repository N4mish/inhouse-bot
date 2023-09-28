import discord # obvious
from discord.ext import commands # has bot class + permissions
import datetime # time for scheduling
import asyncio # async wait
from inhousemanager import InhouseManager # see InhouseManager class - encapsulates scheduling
from inhouse import Inhouse, InhouseBotType, Role # Necessary Enums + Inhouse type
from dateutil import parser # easy parsing of random format times
from dateutil.tz import gettz # timezone getting (it's weird)
import motor
from motor.motor_tornado import MotorClient



""" HELPER CLASSES """
class InterestCheck(discord.ui.View):
    """
    The view class for the interest check message. This has buttons and 
    encompasses all the logic for scheduling, removing and adding people.
    """
    def __init__(self, inhouse: Inhouse, inhouse_manager: InhouseManager, bot: commands.Bot, channel: int):
        super().__init__()
        self.inhouse = inhouse
        self.inhouse_manager = inhouse_manager
        self.bot = bot;
        self.channel = channel;

    @discord.ui.button(label="Yes!", style=discord.ButtonStyle.primary)
    async def add_player(self, interaction, button):
        """
        Function associated with the yes button to add the player to the inhouse.
        Checks how many people are in the inhouse before deciding whether to schedule
        it or not.
        """
        if interaction.user not in self.inhouse.participants:
            await interaction.response.send_message("You've been added to the inhouse list!", ephemeral=True)
            await interaction.user.send("You have been added to the inhouse at a time!")

            self.inhouse.participants.append(interaction.user)
            
            if len(self.inhouse.participants) >= 10:
                await self.inhouse_manager.cancel("test")
                await self.inhouse_manager.schedule(Inhouse(self.inhouse.id, InhouseBotType.INHOUSE, self.inhouse.time))
                await self.bot.get_channel(self.channel).send(f"Inhouses have been scheduled for {self.inhouse.time}!");
        else:
            await interaction.response.send_message("You're already in the inhouse list!", ephemeral=True)
        print(self.inhouse.participants)
    
    @discord.ui.button(label="Remove me", style=discord.ButtonStyle.danger)
    async def remove_player(self, interaction, button):
        """
        Removes player from inhouse if they're present.
        """
        if interaction.user in self.inhouse.participants:
            await interaction.response.send_message("You've been removed from the inhouse list!", ephemeral=True)
            await interaction.user.send(f"You've been removed from inhouse {self.inhouse.id} on {self.inhouse.time}.")
            self.inhouse.participants.remove(interaction.user)
        else:
            await interaction.response.send_message("You were not in the list for this inhouse. No action was taken.", ephemeral=True)
        print(self.inhouse.participants)




""" HELPER ASYNC FUNCTIONS """




async def schedule_ic_wait(client: commands.Bot, inhouse_manager: InhouseManager, ic_time:datetime.datetime, inhouse_time:datetime.datetime):
    """
    Function to schedule interest check and then send message. Each call to this function
    "schedules" a check, basically waiting until the time of the check. Then at the
    time of the call, it makes sure the check is still valid (wasn't canceled) and 
    proceeds with action if it is still valid.
    """
    now = datetime.datetime.now()
    now = now.replace(tzinfo=gettz("America/Chicago")) # assumes your time is CST
    print(f"now: {now} then: {ic_time}")
    wait_time = (ic_time - now).total_seconds()
    await asyncio.sleep(wait_time)

    # schedules the inhouse
    if ic_time in inhouse_manager.timemap:
        temp = inhouse_manager.timemap.pop(ic_time)
        inhouse = Inhouse(temp.id, InhouseBotType.INHOUSE, inhouse_time)
        channel = 1119693446890922016
        await client.get_channel(channel).send(f"Interest check! Please react to this message if you'd like to play inhouse {inhouse.id} on this date!", view=InterestCheck(inhouse, inhouse_manager, client, channel))
        inhouse_manager.idmap.pop(temp.id)
        await schedule_inhouse_wait(client, inhouse_manager, inhouse_time)
    else:
        await client.get_channel(channel).send("That IC was canceled. :(") 
    return


async def schedule_inhouse_wait(client: commands.Bot, inhouse_manager: InhouseManager, time:datetime.datetime):
    """
    Function to schedule inhouse and then send message. Each call to this function
    "schedules" an inhouse, basically waiting until the time of the inhouse. Then at the
    time of the call, it makes sure the inhouse is still valid (wasn't canceled) and 
    proceeds with action if it is still valid.
    """
    now = datetime.datetime.now()
    now = now.replace(tzinfo=gettz("America/Chicago"))
    print(f"now: {now} then: {time}")
    wait_time = (time - now).total_seconds()
    await asyncio.sleep(wait_time)
    channel = 1119693446890922016

    # activating the inhouse
    if time in inhouse_manager.timemap:
        inhouse = inhouse_manager.timemap[time]
        channel = 1119693446890922016
        await client.get_channel(channel).send(f"Inhouse time! Inhouse {inhouse.id} is ready!") 
        temp = inhouse_manager.timemap.pop(time)
        inhouse_manager.idmap.pop(temp.id)
    else:
        await client.get_channel(channel).send("That inhouse was canceled. :(") 
    return




""" MAIN FUNCTION """




def run_discord_bot():
    TOKEN = '' # remove before commit 
    client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
    inhouse_manager = InhouseManager()
    try:
        ibdb = MotorClient("mongodb://localhost:27017/")["InhouseBot"]
    except:
        print("Couldn't Connect to Mongo")


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
    
    @client.tree.command(name='shutdown', description='Shuts down the bot.')
    async def shutdown(interaction: discord.Interaction):
        await interaction.response.send_message(content='Shutting down the bot.')
        await client.close()

    """ ADMIN COMMAND """
    # Please specify date and time in the following format: M/DD/YYYY HH:MM:SS Timezone (in 24h time)
    @client.tree.command(name='scheduleic', description='Schedules an inhouse message and reminders.')
    async def scheduleIC(interaction: discord.Interaction, id: str, ic_time: str, inhouse_time: str):
        try:
            print(ic_time)
            if ic_time.lower().strip() == 'now':
                then = datetime.datetime.now().replace(tzinfo=gettz("America/Chicago"))
            else:
                then = parser.parse(ic_time, tzinfos={"CST": gettz("America/Chicago"), "CDT": gettz("America/Chicago")})
                if then.tzinfo is None:
                    then = then.replace(tzinfo=gettz("America/Chicago"))

            inhouse_datetime = parser.parse(inhouse_time, tzinfos={"CST": gettz("America/Chicago"), "CDT": gettz("America/Chicago")})       
        except:
            await interaction.response.send_message(content=f"Could not schedule inhouse. Time in invalid format. Please specify date and time in the following format: M/DD/YYYY HH:MM:SS Timezone (in 24h time)")
            return
        await inhouse_manager.schedule(Inhouse(id, InhouseBotType.IC, then))
        await interaction.response.send_message(content='Your inhouses have been scheduled!')
        await schedule_ic_wait(client, inhouse_manager, then, inhouse_datetime)
        
    """ ADMIN COMMAND """
    # Please specify date and time in the following format: M/DD/YYYY HH:MM:SS Timezone (in 24h time)
    @client.tree.command(name='scheduleinhouse', description='Schedules an inhouse message and reminders.')
    async def scheduleInhouse(interaction: discord.Interaction, id: str, time: str):
        try:
            print(time)
            if time.lower().strip() == 'now':
                then = datetime.datetime.now().replace(tzinfo=gettz("America/Chicago"))
            else:
                then = parser.parse(time, tzinfos={"CST": gettz("America/Chicago"), "CDT": gettz("America/Chicago")})
                if then.tzinfo is None:
                    then = then.replace(tzinfo=gettz("America/Chicago"))
        except:
            await interaction.response.send_message(content=f"Could not schedule inhouse. Time in invalid format. Please specify date and time in the following format: M/DD/YYYY HH:MM:SS Timezone (in 24h time)")
            return
        await inhouse_manager.schedule(Inhouse(id, InhouseBotType.INHOUSE, then))
        await interaction.response.send_message(content='Your inhouses have been scheduled!')
        await schedule_inhouse_wait(client, inhouse_manager, then)

    """ ADMIN COMMAND """
    @client.tree.command(name='cancel', description='Cancels an inhouse given an id.')
    async def cancel(interaction: discord.Interaction, id: str):
        id = id.strip()
        res = await inhouse_manager.cancel(id)
        if res:
            await interaction.response.send_message(content=f"Canceled inhouse with id {id}.")
        else:
            await interaction.response.send_message(content=f"Inhouse with id {id} does not exist or an error occurred.")
    
    @client.tree.command(name='set_channel', description='Sets the inhouse bot channel to the specified channel.')
    async def set_channel(interaction: discord.Interaction, channel: discord.TextChannel):
        await ibdb['ChannelIDs'].update_one({"GuildID":interaction.guild_id}, {"$set": {"channel":channel.id}})
        await interaction.response.send_message(f"{interaction.guild.name}'s channel has been set to {channel.name}!")

    @client.tree.command(name='set_role_prefs', description='Sets the number role preference to the role you specify.')
    async def set_role_prefs(interaction: discord.Interaction, pref: int, role: Role):
        default = {"1":Role.TOP.value, "2":Role.JGL.value, "3":Role.MID.value, "4":Role.ADC.value, "5":Role.SUP.value} # default role prefs
        ct = await ibdb['RolePrefs'].count_documents({"id":interaction.user.id})
        if ct > 0:
            await ibdb['RolePrefs'].update_one({"id": interaction.user.id}, {"$set": {pref:role}})
        else:
            default[str(pref)] = role.value
            default["id"] = interaction.user.id
            await ibdb['RolePrefs'].insert_one(default)
        await interaction.response.send_message("Your role preferences have been updated!", ephemeral=True)
        


    client.run(TOKEN)

    # scheduling. for future use, integrate this with database to find stored times based on server.
