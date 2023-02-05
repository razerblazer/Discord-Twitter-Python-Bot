# Discord-Twitter-Python-Bot
This bot uploads the URL of any recent Twitter posts made by a user. A discord channel has the ability to "subscribe" to any specific Twitter user and the bot will alert that specific channel of any new Tweets made by that particular user.

# NOTICE
Due to twitter getting rid of the free tier for api access, you will unfortunately have to pull out your precious wallet if you want things to work.

# Command and Implementation Details
The bot uses the Tweepy.py API to access the needed [twitter data](https://twitter.com/). The bot is always on standby and reacts to specific messages that contains the special $ character and carries out the action based on what was given. When a channel requests to "watch" a specific Twitter user's Tweets, the bot will keep track of the channel objects that made this request per Twitter user. The bot stores the id of the most latest tweet and it makes a request at a set time interval to return the id of the most recent twitter post for that user. If the user has indeed posted a new Tweet, the bot will generate a link to that specifc tweet for that user and notify all channels that have requested them. There is a secondary dictionary that stores all guild and channel ids that are associated per twitter user so that if the bot were to be restarted, all the stored channel objects do not have to be reentered in again. 
# Current Implemented Commands:
- `$subscribe ______ _____(integer value)`: The user can type in a Twitter screen name/username for the bot to keep track of that particular user and post any new tweets in the discord channel this command was requested from.
- `$unsubscribe ______`: The user can similarly type in this command to stop tracking the posts of a particular user that the discord channel is already subscribed to.
- `$listsubs`: This command will generate a discord embed that lists all of the twitter users the channel is subscribed to in the channel this command was typed in. 

# Bug Fixes(definitely just features) and New Stuff:
- v1.1(I guess?) fixed issue where the bot subscribed to a user with no tweets in their timeline would return emptylist which resulted in a error when running through the dictionary
- v2.0 Added mode 1 or 2 as posting options. Option 1 will post all activity of that twitter user, option 2 posts everything except for replies. If user subscribes without specifying mode, bot will default that user to mode 1. Currently only way to change modes is to unsubscribe and resubscribe with the desired mode. Will add a change mode feature sometime in the future. 
- v2.1 Added a way for the bot to store data inside of latest tweet made by user dictionary. Added mode 3 and reversed order of modes(mode 3 is all activity, mode 2 is only tweets and retweets and mode 1 is tweets made by that user only). Found issue with case sensitive string comparisons when checking dictionary(now uses .lower() on all incoming inputs and storing of string). Will likely change stringly typed logic later on. Next step is adding mutex locks to dictionaries to prevent unknown errors from occuring. 
