# Discord-Twitter-Python-Bot
This bot uploads the URL of any recent Twitter posts made by a user. A discord channel has the ability to "subscribe" to any specific Twitter user and the bot will alert that specific channel of any new Tweets made by that particular user.

# Command and Implementation Details
The bot uses the Tweepy.py API to access the needed twitter data. The bot is always on standby and reacts to specific messages that contains the special $ character and carries out the action based on what was given. When a channel requests to "watch" a specific Twitter user's Tweets, the bot will keep track of the channel objects that made this request per Twitter user. The bot stores the id of the most latest tweet and it makes a request at a set time interval to return the id of the most recent twitter post for that user. If the user has indeed posted a new Tweet, the bot will generate a link to that specifc tweet for that user and notify all channels that have requested them. There is a secondary dictionary that stores all guild and channel ids that are associated per twitter user so that if the bot were to be restarted, all the stored channel objects do not have to be reentered in again. 
# Current Implemented Commands:
- `$subscribe ______`: The user can type in a Twitter screen name/username for the bot to keep track of that particular user and post any new tweets in the discord channel this command was requested from.
- `$unsubscribe ______`: The user can similarly type in this command to stop tracking the posts of a particular user that the discord channel is already subscribed to.
- `$listsubs`: This command will generate a discord embed that lists all of the twitter users to the channel this command was typed in. 
