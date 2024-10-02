from datetime import datetime, timedelta
import functools
import time
import typing
import discord
from discord.ext.commands import Bot
import os
import webbrowser
import FantasyFunctions
import secrets

POST_NOW = False # SET ME TO FALSE TO POST AT 9AM PST
CHANNEL_ID = 866871591216480256 #TESTING: 1203254371262005269 || WEEKLY STATS: 866871591216480256

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
client = discord.Client(intents=intents)

async def PrintStats():
    statsChannel = client.get_channel(CHANNEL_ID) 

    result = "WEEK " + str(FantasyFunctions.WEEK_NUM) + " STATS\n"
    result += FantasyFunctions.GetStandings(client) + "\n"
    result += FantasyFunctions.GetMatchupScores(client)
    await statsChannel.send(result)
    print("Printed Standings and Scores\n    Characters: " + str(len(result)) + "/2000")
    result = FantasyFunctions.GetTopScorers(client) + "\n"
    result += FantasyFunctions.GetBottomScorers(client) + "\n"
    result += FantasyFunctions.GetHardestSchedule(client) + "\n"
    result += FantasyFunctions.GetSoftestSchedule(client) + "\n"
    result += FantasyFunctions.GetTopWeeklyScorers(client) + "\n"
    result += FantasyFunctions.GetBottomWeeklyScorers(client) + "\n" + "\n"
    await statsChannel.send(result)
    print("Printed Top/Bottom Seasonal and Weekly Scorers\n    Characters: " + str(len(result)) + "/2000")
    result = FantasyFunctions.GetBiggestBlowout(client) + "\n"
    result += FantasyFunctions.GetClosestWin(client) + "\n"
    result += FantasyFunctions.GetMostPtsInALoss(client) + "\n"
    result += FantasyFunctions.GetLeastPtsInAWin(client) + "\n"
    result += FantasyFunctions.GetBestLuck(client) + "\n"
    result += FantasyFunctions.GetWorstLuck(client) + "\n"
    result += FantasyFunctions.GetBestBench(client) + "\n"
    result += FantasyFunctions.GetWorstBench(client) + "\n"
    result += FantasyFunctions.GetUpsets(client) + "\n" + "\n"
    await statsChannel.send(result)
    print("Printed Blowout/Closecall, Luck, Bench, Upsets\n    Characters: " + str(len(result)) + "/2000")
    #players
    result = FantasyFunctions.GetBestStartingPlayers(client) + "\n"
    result += FantasyFunctions.GetBestBenchPlayers(client) + "\n" + "\n"
    await statsChannel.send(result)
    print("Printed player stats\n    Characters: " + str(len(result)) + "/2000")
    #managers
    result = FantasyFunctions.GetMostEfficientManager(client) + "\n"
    result += FantasyFunctions.CouldHaveWonIf(client)
    await statsChannel.send(result)
    print("Printed manager stats\n    Characters: " + str(len(result)) + "/2000")

async def AssignWinnersAndLosers():
    server = discord.utils.get(client.guilds, id=866871459473522708)
    winnerRole = server.get_role(866871899480522784)
    loserRole = server.get_role(866871975237124197)
    for team in FantasyFunctions.GetWinnerIds():
        user = FantasyFunctions.team_to_user.get(team)
        if user == None:
            print("TEAM ID SOMEHOW NOT FOUND: " + team)
        else:
            member = server.get_member(user)
            
            await member.add_roles(winnerRole)
            await member.remove_roles(loserRole)

    for team in FantasyFunctions.GetLoserIds():
        user = FantasyFunctions.team_to_user.get(team)
        if user == None:
            print("TEAM ID SOMEHOW NOT FOUND: " + team)
        else:
            member = server.get_member(user)
            
            await member.add_roles(loserRole)
            await member.remove_roles(winnerRole)

async def WipeWinnersLounge():
    server = discord.utils.get(client.guilds, id=866871459473522708)
    currentLounge = discord.utils.get(server.channels, name="winners-lounge")
    await currentLounge.clone(reason="Wiping The Lounge")
    await currentLounge.delete()


async def AssignSeedsToNicknames():
    server = discord.utils.get(client.guilds, id=866871459473522708)
    sortedTeams = FantasyFunctions.GetTeamIdsSorted()

    for i in range(len(sortedTeams)):
        team = sortedTeams[i]
        user = FantasyFunctions.team_to_user.get(team)
        nickname = FantasyFunctions.team_to_name.get(team)
        member = server.get_member(user)
        await member.edit(nick= "#" + str(i + 1) + " " + nickname)



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Now able to fetch fantasy stats, commish')


    print("Wait Completed - let's get cookin'")
    await client.change_presence(status=discord.Status.online)
    await PrintStats()
    print("Printed Stats")
    await AssignWinnersAndLosers()
    print("Assigned winners and losers")
    await AssignSeedsToNicknames()
    print("Changed seeds in nicknames")
    await WipeWinnersLounge()
    print("Wiped the winners lounge")
    print("Weekly tasks completed!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('sleep tight lil statbot'):
        await message.channel.send('zzz :sleeping:')


## RUNNING THE ACTUAL BOT
## we start with a wait until the time I wanna post the stats :)
print("Calculating how long to wait...")
time.sleep(1)
    
startTime = datetime.today()
weekday = startTime.weekday() # 0 is Monday, 6 is Sunday for day
postTime = startTime

# This is a dumb way of doing it but I'm high and can't figure out something better rn
if (POST_NOW):
    time_change = timedelta(seconds=1)
    postTime = startTime + time_change
elif (weekday == 0): # it is Monday (day before post needs to happen, add 1)
    postTime = (startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days = 1))
elif (weekday == 1): # it is Tuesday (day post needs to happen, add 0)
    postTime = startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0)
elif (weekday == 2): # it is Wednesday
    postTime = (startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days = 6))
elif (weekday == 3): # it is Thursday
    postTime = (startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days = 5))
elif (weekday == 4): # it is Friday
    postTime = (startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days = 4))
elif (weekday == 5): # it is Saturday
    postTime = (startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days = 3))
else: # it is Sunday
    postTime = (startTime.replace(day=startTime.day, hour=9, minute=0, second=0, microsecond=0) + timedelta(days = 2))

deltaTime = postTime - startTime
deltaTimeSeconds = deltaTime.total_seconds()

print("Waiting " + str(deltaTimeSeconds) + " seconds...")
time.sleep(deltaTimeSeconds)
client.run(secrets.TOKEN)






