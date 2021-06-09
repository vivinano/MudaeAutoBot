Please Gif Star ?? Stars make me happy.  I'm open to design automation for other games (doesn't have to be a discord game) just let me know

# Regarding Issue Creation
Lately I have been getting alot of **Issues** that is not based on problems with the bot but they regard `Python Enviroment Errors` I.E `discum module not found`/`discum not installed properly` I have attempted to help many users that have had this problem but it is very time consuming. Python Enviroment issues are not a problem with the **BOT** but how one has installed python this varies from user to user.There are archived issues where a user has had a enviroment issue and they have resolved it you can use that as a reference.
If these resources do not help there are plently of resources online to help you resolve your `Python Enviroment` Issue

**Future Issues opened that do NOT deal with a Error with the BOT will be labeled accordingly and closed**

# MudaeAutoBot
MudaeAutoBot is a python bot that auto rolls and attempts to snipe Kakeras and Claims in Mudae

# Features
+ Snipes and claims Kakera in any Discord servers you're in that has Mudae#0807
+ Kakera value sniping as long as kakera value can be determined (e.g. Like Rank, Claim Rank, ## Kakera)
+ Maximizes rolls by tracking roll timers
+ Waifu/Husbando rolling
+ Pokeslot rolling
+ Selective Kakera Reaction Snipes Features(Includes: Soulmate Kak sniping Feature)
+ Mudae emoji reaction event sniping support

## How it works
All this bot needs to work is your Discord _usertoken_ and the channel IDs that you want it to post in

This is intended to be completely automated; it doesn't need to take any input other than initial settings configuration.
You'll be able to leave the window running in the background, and not need to think about it.

## Requirements

+ Python 3.7+
+ discum 1.3+

# Configuration
To configure the bot, you'll edit the variables in the **Settings_Mudae.json** file for your botting needs.

## Bot settings
All settings are set within the Settings_Mudae.json File

+ `token` - The user token for the account you want to bot on. If you need extra assistance on how to obtain it, let me know.
+ `channelids` - Which channels to **roll** and **monitor**  e.g. 807##########948
+ `claim_delay` - _Affects all servers_ Time in **seconds** to wait before attempting to Claim Characters e.g. 5
+ `kak_delay` - _Affects all servers_ Time in **seconds** to wait before attempting to snipe Kakeraloot e.g. 8
+ `use_emoji` - This setting only works if you change the Mudaebot.py code by uncommenting out the line (Custom emojis only) e.g.  "<:emoji_name:795############214>"
+ `roll_this` - ($m|$ma|$mg|$w|$wg|$wa|$h|$ha|$hg) If `Rolling` is enabled it will roll this specific command e.g. '$wg'
+ `Rolling` - (True|False) **Case-sensitive**, uses `channelid`
+ `PkmRolling` - (True|False) Pokeslot rolling enabled, uses `channelid`
+ `series_list` - **Case-sensitive** Name of series of characters you want to claim  e.g. \[ "Honkai Impact 3rd" , "Senran Kagura" \]
+ `name_list` - **Must be exact match** List of specific character names to claim  e.g. \["Raiden Mei", "gOkU" \]
+ `emoji_list` - This is the kakera that will be snipes \[ "KakeraY" , "KakeraO" \] << This example means only snipe Yellow and orange Kakera
+ `min_kak` - A minimum kakera value to snipe a claimable character _regardless of whether it's in the series/name lists_

# Optimize the snipes
Typing $settings in your server with mudae should give you the snipe and kaksnipping timers.
Using these values you usually snipes faster than a "Human" user can react 

Please when settings Delays avoid setting 0 as your delay as it might be to fast for mudae
a minimum of 1 second to let mudae register that a character was rolled as is reacted to.

# Use at your own Risk
This is a Discord **selfbot**. I am not responsible if you get banned using this program. 

# Buy me a coffee
At the request of my personal friends they insisted me link a way to make money off of this project so I guess if you like the support I offer you can always buy me some food or snacks.
https://www.paypal.com/donate?hosted_button_id=ALRBET9746T8W

# Closing Notes
I understand that this readme is not as detailed as many would like and I'm sure there are many more questions that one may have.

Currently I'm still supporting this repo so feel free to **Contact Me** if you are having any Issues (Setup , Bugs , Feature suggestions)

As for updates those will be added up until I no longer feel like this project is fun.

Thanks to:
https://github.com/FatPain
for Assisting with Discum it was definitly not something I'm use to

