Please Gif Star ?? Stars make me happy
# Current issues
Limited channel is just gonna be the default method. users can remove that check if they want all servers. Current issue is that when using for prolong periods of time discum might stop causing rolling functions to break and spam server. Checking with (auto_reconnect=True) and seeing if run into this issue after a longetivity stress test 


Thanks to:
https://github.com/FatPain
for Assisting with Discum it was definitly not something I'm use to


# MudaeAutoBot
What is Mudae Auto Bot?

it is a python bot that Auto rolls and attempts to snipe kaks and Claims in Mudae

How does it work?

All this bot need to work is your "Discord" usertoken and the channel ID that you want to post in

How Automated is it ?

This is completely automated it doesnt need to take any input after inital set up.
I made it simple where all the variables you need can be edited within the **setting_mudae.json** file
Your able to run MudaeAutoBot and still be able to do normal work on your device

# Features
+ Snipes and claims kak in all Discord servers you are in that has Mudae#0807
+ Kak Value sniping as long as Kak value can be determined (Like Rank , Claim Rank , ## Kakera)
+ Waifu/Husbando Rolling Features that Dynamically grab roll timers
+ Pokeslot Rolling Features that Dynamically grab roll timers
+ Selective Kakera Reaction Snipes Features(Includes: Soulmate Kak sniping Feature)
+ Emoji Reaction Snipes  **Ex:Mudae Events**


+ MultiRolling Support was added !!!! (please note that each channel will open a Background_task and is not True Threading there will be Issues) **Go Overboard at your own risk**

# Setting up the bot
All settings are within the Settings_Mudae.json File

+ 1. token - **User token** basically the account you want to run this on. If you need extra assistance on how to obtain it let me know.
+ 2. channelid - Which channel to **Roll** in only (Might Have more uses in the future) ex. 807##########948
+ 3. multichannel - Which Channel(s) to **Roll** in only (Might havre more uses in future) ex.\[ 807##########948, 517########420\]
+ 4. claim_delay - Universal-Wide time in **secs** to wait before attempting to Claim Characters ex. 5
+ 5. kak_delay - Universal-Wide time in **secs** to wait before attempting to snipe Kakeraloot ex. 8
+ 6. use_emoji - This setting only works if you change the Mudaebot.py code by uncommenting out the line (Custom emojis only) ex.  "<:emohi_name:795############214>"
+ 7. roll_this - If Rolling Enabled it will roll ($m|$ma|$mg|$w|$wg|$wa|$h|$ha|$hg)
+ 8. Rolling - (True|False) **case sensetive** , Uses ChannelId
+ 9. Multirollenable - (True|False) **Case Sensetive** !!Rolling must be set to False if MultiRollEnable is True!!
+ 10. PkmRolling - (True|False) Pokeslot rolling enabled, Uses Channelid
+ 11. series_list - Name of series of characters you want to claim **Case Sensetive** ex \[ "Honkai Impact 3rd" , "Senran Kagura" \]
+ 12. name_list - Character name to claim **Exact match only** ex \["Raiden Mei", "gOkU" \]
+ 13. SoulmateKakSnipeOnly - (True|False) **Case Sensetive** End-game setting to snipe soulmate kakera
+ 14. SoulmateKakColorValue - #HexValue this is for Soulmate Kakera snipe same value as $ec in Mudae. This is to help determine which one is yours vs soulmate of others
+ 15. emoji_list - This is the kakera that will be snipes \[ "KakeraY" , "KakeraO" \] << This example means only snipe Yellow and orange Kakera
+ 16. min_kak - Claim Character that has a Kakera Worth > Minimum value ex. 500 
 
 
 ** In the limited version you need to set multiids for channel you want to monitor ** 
orginally I didn't want this set up process to be needed as it was easier for someone to set up a user token with the default settings and spin it right up but with more users requesting the limited scope I made the option avaible in a seperate code file
# Optimize the snipes
Typing $settings in your server with mudae should give you the snipe and kaksnipping timers.
Using these values you usually snipes faster than a "Human" user can react 

Please when settings Delays avoid setting 0 as your delay as it might be to fast for mudae
a minimum of 1 second to let mudae register that a character was rolled as is reacted to.

(Keep in mind that changing Delays effect servers across the board not just 1 Server)

# Requirments
*Python installed

--python extras--

+ python std library (comes with your python install)
+ discum 

--legacy--
+ discord.py 


# Use at your own Risk
This is a Discord **selfbot**. I do not claim any responsiblity for bans that happen from use of this program

Even though Discord.py is used to make normal bots and the only difference is the token used (Bot Token, User Token)
This is still a Selfbot 

# Closing Notes
I understand that this readme is not as detailed as many would like and I'm sure there are many more questions that one may have.

Currently I'm still supporting this repo so feel free to **Contact Me** if you are having any Issues (Setup , Bugs , Feature suggestions)

As for updates those will be added up until I no longer feel like this project is fun.

# Buying me a coffee

At the request of my personal friends they insisted me link a way to make money off of this project so I guess if you like the support I offer you can always buy me some food or snacks.
https://www.paypal.com/donate?hosted_button_id=ALRBET9746T8W
