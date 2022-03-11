import tweepy
import discord
import time
import schedule
import threading
import asyncio
import json
import os
import sys
import ast

#discord bot login credentials
TOKEN = "discord bot token"
intents = discord.Intents.all()
client = discord.Client(intents=intents)



datastore = {}  #'twitter user': 'discord channels that requested this user'
secondaryfilestore= {}
globaltweetstore = {}

#twitter api login credentials
auth= tweepy.OAuthHandler("credentials")
auth.set_access_token("some more credentials")
api= tweepy.API(auth)


#save dictionary file management, create new file if it doesnt exist
a = open("storetwittersubs.txt", "a")
a.close()

b = open("latest_tweet_data.txt", "a")
b.close()


async def twitter_channel_init():
    await client.wait_until_ready()
    global globaltweetstore
    fileinfo = os.path.getsize("storetwittersubs.txt")
    if fileinfo != 0:
        file = open("storetwittersubs.txt", "r")
        content = file.read()
        txtcontent = ast.literal_eval(content)

        for user in txtcontent:
            if user not in datastore:
                datastore[user] = []
            for channel in txtcontent[user]:
                datastore[user].append((client.get_guild(channel[0]).get_channel(channel[1]), channel[2]))
            if user not in secondaryfilestore:
                secondaryfilestore[user] = []
            for chan in txtcontent[user]:
                secondaryfilestore[user].append((chan[0], chan[1], chan[2]))
        file.close()
    fileinfo2 = os.path.getsize("latest_tweet_data.txt")
    if fileinfo2 != 0:
        file2 = open("latest_tweet_data.txt", "r")
        content2 = file2.read()
        txtcontent2 = ast.literal_eval(content2)
        globaltweetstore = txtcontent2
        file2.close


async def twitter_management():
    global datastore
    global globaltweetstore
    for c in datastore.keys():
        last_tweet = globaltweetstore[c] if c in globaltweetstore.keys() else None
        tweet = get_latest_tweet(c)
        if tweet is None:
            continue
        if tweet.id == last_tweet:
            continue
        globaltweetstore[c] = tweet.id
        for u in datastore[c]:
            if tweet.in_reply_to_status_id_str is not None:
                if u[1] == "3":
                    await u[0].send("Here is @"+ tweet.user.screen_name + "'s latest tweet! This is a reply to either a tweet or comment!\n"+ "https://twitter.com/"+ tweet.user.screen_name + "/status/" + tweet.id_str)
                    continue
                else:
                    continue
            if hasattr(tweet, 'retweeted_status') is True:
                if (u[1] == "3") or (u[1] == "2"):
                    await u[0].send("Here is @" + tweet.user.screen_name + "'s latest tweet! This is a retweet of user @" + tweet.retweeted_status.user.screen_name + "'s tweet!\n" + "https://twitter.com/"+ tweet.retweeted_status.user.screen_name + "/status/" + tweet.retweeted_status.id_str)
                    continue
                else:
                    continue
            await u[0].send("Here is @"+ tweet.user.screen_name + "'s latest tweet!\n" + " https://twitter.com/"+ tweet.user.screen_name+ "/status/" + tweet.id_str)
    copy_twitter_data_to_file()
    
    
def get_latest_tweet(user):
    try:
        return next(tweepy.Cursor(api.user_timeline, screen_name=user).pages())[0]
    except:
        return None
    
def valid_usertest(user):
    try:
        api.get_user(screen_name=user)
        if api.get_user(screen_name=user).protected:
            return False
    except:
        return False
    return True

def check_dictionary(channel, user):
    for a in datastore[user]:
        if a[0] == channel:
            return False
    return True

def copylocaldictioarytofile():
    global secondaryfilestore
    fileaccess = open("storetwittersubs.txt","r+")
    filedata = os.path.getsize("storetwittersubs.txt")
    if filedata != 0:
        fileaccess.truncate(0)
    fileaccess.write(json.dumps(secondaryfilestore))
    fileaccess.close()
    
def copy_twitter_data_to_file():
    global globaltweetstore
    fileaccess = open("latest_tweet_data.txt", "r+")
    filedata = os.path.getsize("latest_tweet_data.txt")
    if filedata != 0:
        fileaccess.truncate(0)
    fileaccess.write(json.dumps(globaltweetstore))
    fileaccess.close()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'{client.user} is connected to the following guild:\n{guild.name}(id: {guild.id})')
        members = '\n - '.join([member.name for member in guild.members])
        print(f'Guild Members:\n - {members}')


@client.event
async def on_message(message):
    try:
        print(message.content, message.author.id, client.user.id, message.channel.id, message.guild.id)
        global garfcountlimiter
        global datastore
        global secondaryfilestore
        global globaltweetstore
        if message.author.id == client.user.id:
            return
    #twitter stuff section
        if message.content.startswith("$subscribe"):
            try:
                if message.content.split(" ")[0] != "$subscribe":
                    return await message.channel.send("Did you mean $subscribe?")
                bananasplit = message.content.split(" ")
                if len(bananasplit) == 3:
                    usernamestore = bananasplit[1].lower()
                    mode = bananasplit[2]
                    if (mode != '1') and (mode != '2') and (mode != '3'):
                        return await message.channel.send("Please enter a valid mode number!")
                else:
                    usernamestore = bananasplit[1].lower()
                    mode = '1'
            except:
                await message.channel.send("Did you even try to enter in a twitter username lol")
                return
            if usernamestore.startswith("@"):
                return await message.channel.send("You do not require the @ symbol!")
            if valid_usertest(usernamestore):
                if usernamestore in datastore.keys() and check_dictionary(message.channel, usernamestore):
                    datastore[usernamestore].append((message.channel, mode))
                    secondaryfilestore[usernamestore] = [(message.guild.id, message.channel.id, mode)]
                    await message.channel.send("Twitter Posts from @" + usernamestore + " will now be posted in this channel!")
                    copy_local_dictionary_to_file()
                    return
                elif usernamestore not in datastore:
                    datastore[usernamestore] = [(message.channel, mode)]
                    secondaryfilestore[usernamestore] = [(message.guild.id, message.channel.id, mode)]
                    await message.channel.send("Twitter Posts from @" + usernamestore + " will now be posted in this channel!")
                    copy_local_dictionary_to_file()
                    return
                else:
                    await message.channel.send("This channel is already subscribed to this user!")
                    return
            return await message.channel.send("The provided Twitter username is either invalid or they have a private profile!")
        if message.content.startswith("$unsubscribe"):
            try:
                if message.content.split(" ")[0] != "$unsubscribe":
                    return await message.channel.send("Did you mean $unsubscribe?")
                usernamestore2 = message.content.split(" ")[1].lower()
            except:
                await message.channel.send("Did you even try to enter in a twitter username lol")
                return
            if usernamestore2.startswith("@"):
                return await message.channel.send("You do not require the @ symbol!")
            if valid_usertest(usernamestore2):
                for a in datastore:
                    for b in datastore[a]:
                        if (b[0] == message.channel) and (a == usernamestore2):
                            datastore[a].remove(b)
                            copy_local_dictionary_to_file()
                for s in secondaryfilestore:
                    removaltracker = []
                    for chan_id in secondaryfilestore[s]:
                        if (chan_id[1] == message.channel.id) and (s == usernamestore2):
                            secondaryfilestore[s].remove(chan_id)
                            if secondaryfilestore[s] == []:
                                removaltracker.append(s)
                            for removalelement in removaltracker:
                                del secondaryfilestore[removalelement]
                                del globaltweetstore[removalelement]
                            await message.channel.send("@" + usernamestore2 + " has successfully been unsubscribed from this channel! Posts from this user will no longer be posted here.")
                            copy_local_dictionary_to_file()
                            copy_twitter_data_to_file()
                            return
                await message.channel.send("This channel is currently not subscribed to this user! Use $subscribe to subscribe this channel to that user.")
                return
            else:
                await message.channel.send("The provided twitter username is invalid!")
                return
        if message.content.startswith("$listsubs"):
            chansubs = []
            messageembed = discord.Embed(title="Twitter users this channel is currently subscribed to")

            for users in secondaryfilestore:
                for chanid in secondaryfilestore[users]:
                    if message.channel.id == chanid[1]:
                        chansubs.append((users, chanid[2]))
            if len(chansubs) == 0:
                await message.channel.send("This channel is currently not subbed to any Twitter users! Type $subscribe \"twitter username\" (without the quotations) to sub to a user!")
                return
            else:
                for subbedpeople in chansubs:
                    twitterinfo = get_latest_tweet(subbedpeople[0])
                    messageembed.add_field(name=(twitterinfo.user.name + " (mode " + subbedpeople[1] + ")"), value="@" + subbedpeople[0])
            return await message.channel.send(embed=messageembed)
        if message.content == "print twitterlist":
            print(datastore)
            print(secondaryfilestore)
            print(globaltweetstore)
            return

#misc commands and debugging code
    if message.content == 'testdm':
        await message.author.create_dm()
        await message.author.dm_channel.send('lol it works')
        return
    if message.content.startswith("$help"):
        embed = discord.Embed(title="Currently available commands", description="Contact me if u wanna suggest more functionalities for this server lol")
        embed.add_field(name="Twitter functions:", value="these are current twitter functions that have been implemented")
        embed.add_field(name="$subscribe ____________(enter in a twitter username without the @) ___ <-mode 1,2,3(1 is only tweets by the user, mode 2 is only tweets and retweets and mode 3 is any activity made by the user including replies.)", value="Tracks the listed twitter user and posts any new tweets made by them in the requested discord channel", inline=False)
        embed.add_field(name="$unsubscribe ____________ ^", value="Stops posting tweets by the requested user", inline=False)
        embed.add_field(name="$listsubs", value="Lists all twitter users that are being tracked by this channel", inline=False)
        await message.channel.send(embed=embed)
        return
    if message.content.startswith("$"):
        return await message.channel.send("Either you can't spell or you're just listing how much you lost in your last poker game. Type $help for a list of currently implemented commands.")
    except:
    return await message.channel.send("A fatal flaw has occured somewhere. Please contact _____ for maintenance!")

schedule.every(30).seconds.do(lambda: client.loop.create_task(twittermanagement()))
x = threading.Thread(target=run_scheduler)

client.loop.create_task(twitter_channel_init())
x.start() #check external files for records of already stored subscription data
client.run(TOKEN)
