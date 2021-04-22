import discord
import asyncio
import re
import json
import time


jsonf = open("Settings_Mudae.json")
settings = json.load(jsonf)
jsonf.close()


#Settings
kakera_wall = {}
token = settings["token"]
mudae = 432610292342587392
channelid = settings["channel_id"]
multiids = settings["multichannel"]
claim_delay = settings["claim_delay"]
kak_delay = settings["kak_delay"]
roll_prefix = settings["roll_this"]
kak_min = settings["min_kak"]
soulmatekak = settings["SoulmateKakSnipeOnly"]
eccolor = int(settings["SoulmateKakColorValue"].replace("#",""),16)

wait_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min \w')
waitk_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
kak_finder = re.compile(r'\*\*??([0-9]+)\*\*<:kakera:469835869059153940>')
like_finder = re.compile(r'Likes\: \#??([0-9]+)')
claim_finder = re.compile(r'Claims\: \#??([0-9]+)')
poke_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
#use_emoji = settings["use_emoji"]
use_emoji = "❤️"


series_list = settings["series_list"]
chars = [charsv.lower() for charsv in settings["namelist"]]
KakeraVari = [kakerav.lower() for kakerav in settings["emoji_list"]]
eventlist = ["🕯️","😆"]

def get_wait(text):
    waits = wait_finder.findall(text)
    if len(waits):
        hours = int(waits[0][0]) if waits[0][0] != '' else 0
        return (hours*60+int(waits[0][1]))*60
    return 0

def get_pwait(text):
    waits = poke_finder.findall(text)
    if len(waits):
        hours = int(waits[0][0]) if waits[0][0] != '' else 0
        return (hours*60+int(waits[0][1]))*60
    return 0
    
def get_kak(text):
    k_value = kak_finder.findall(text)
    like_value = like_finder.findall(text)
    claim_value=claim_finder.findall(text)
    if len(k_value):
        return k_value[0]
    elif len(like_value) or len(claim_value):
        LR = 0
        CR = 0 
        CA= 1
        if(len(like_value)):
            LR = like_value[0]
        if(len(claim_value)):
            CR = claim_value[0]
        pkak = (int(LR) + int(CR)) /2
        multi = 1 + (CA/5500)
        return((25000 *(pkak+70)**-.75+20)*multi+.5)     
    return 0

class MyClient(discord.Client):

        
        
    async def on_ready(self):
        print('Logged on as', self.user)
        if settings['pkmrolling'] == "True":
            self.loop.create_task(self.poke_task())
        if settings["rolling"] == "True":
            await asyncio.sleep(8)
            self.loop.create_task(self.bg_task(channelid))
        if settings["rolling"] != "True" and settings["Multirollenable"] == "True":
            await asyncio.sleep(8)
            for multichannel in multiids:
                self.loop.create_task(self.bg_task(multichannel))
                await asyncio.sleep(30)
        
        
            

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
           return

        
        if message.author.id == mudae:
            #print(message.content)
                             
            if message.embeds != []:
                objects = message.embeds[0].to_dict()
                #print(objects.keys())
                if 'author' in objects.keys():
                    charsname = objects['author']['name']
                else:
                    charsname = "jklsdajklasd no author found"
                
                #print(charsname)
                
                
                
                if str(self.user.id) in message.content:
                    print(f"Attempting to Claim {objects['author']['name']} Wished by {self.user.name} in ({message.channel.id}):{message.channel.name}")
                    emoji = use_emoji
                    await asyncio.sleep(claim_delay)
                    await message.add_reaction(emoji)
                
                for ser in series_list:
                    if ser in objects['description']:               
                        print(f"Attempting to Claim {objects['author']['name']} from {ser} in ({message.channel.id}):{message.channel.name}")
                        emoji = use_emoji
                        await asyncio.sleep(claim_delay)
                        await message.add_reaction(emoji)
                        break
                        
                if charsname.lower() in chars:
                    print(f"Attempting to Claim {objects['author']['name']} in ({message.channel.id}):{message.channel.name}")
                    emoji = use_emoji
                    await asyncio.sleep(claim_delay)
                    await message.add_reaction(emoji)
                    
                        
                if "<:kakera:469835869059153940>" in objects['description'] or ("Claims:" in objects['description'] or "Likes:" in objects['description']) :
                    kak_value = get_kak(objects['description'])
                    #print(kak_value)
                    if int(kak_value) >= kak_min and ("**$togglereact**" in objects['description'] or objects['color'] == 16751916):
                        emoji = use_emoji
                        await asyncio.sleep(claim_delay)
                        await message.add_reaction(emoji)
                        print(f"Claming {objects['author']['name']} worth {int(kak_value)} Kakera")
                        
                    
    

    async def on_reaction_add(self,reaction,user):
        if(reaction.custom_emoji and reaction.emoji.name.lower() in KakeraVari) and user.id == mudae:
            if soulmatekak == "True":
                if reaction.message.embeds != []:
                    recCon = reaction.message.embeds[0].to_dict()
                    if "<:chaoskey:690110264166842421>" in recCon['description'] and recCon['color'] == eccolor :
                        await asyncio.sleep(kak_delay)
                        await reaction.message.add_reaction(reaction.emoji)
                        
        if (reaction.custom_emoji and reaction.emoji.name == "kakeraP"):
            await asyncio.sleep(1)
            print(f"{reaction.emoji.name} was detected in {reaction.message.channel.id} : {reaction.message.channel.name}")
            await reaction.message.add_reaction(reaction.emoji)
            await asyncio.sleep(1)
            await reaction.message.remove_reaction(reaction.emoji)
            await asyncio.sleep(kak_delay - 2)
            await reaction.message.add_reaction(reaction.emoji)
                
                
                
        if(reaction.custom_emoji and reaction.emoji.name.lower() in KakeraVari) and user.id == mudae:

            await asyncio.sleep(kak_delay)
            print(f"{reaction.emoji.name} was detected in {reaction.message.channel.id} : {reaction.message.channel.name}")
            cooldown = kakera_wall.get(reaction.message.guild.id,0) - time.time()
            if cooldown <= 1: 
                await reaction.message.add_reaction(reaction.emoji)
            else:
                print(f"Skipping {reaction.emoji.name} in {reaction.message.channel.id} : {reaction.message.channel.name} because on cooldown; {cooldown/60} minutes left")
                return
            def check_this(message):
                return message.author.id == mudae and message.content.startswith(f"**{self.user.name}") and "kakera" in message.content
            try:
                msg = await self.wait_for('message',timeout=10.0,check=check_this)
                time_to_wait = waitk_finder.findall(msg.content)
                if len(time_to_wait):
                    timegetter = (int(time_to_wait[0][0] or "0")*60+int(time_to_wait[0][1] or "0"))*60
                    #print(timegetter)
                    kakera_wall[reaction.message.guild.id] = timegetter + time.time()
            except asyncio.TimeoutError:
                pass
                
        
        if (user.id == mudae and not reaction.custom_emoji):
            if reaction.emoji in eventlist:
                await asyncio.sleep(kak_delay)
                await reaction.message.add_reaction(reaction.emoji)
                
            
            
    async def bg_task(self,taskid):
        rollingchannel = self.get_channel(taskid)
        wait = 0
        def msg_check(message):
            return message.author.id == mudae and message.channel.id == taskid
        
        while True:
            while wait == 0:
                wait_for_mudae = self.loop.create_task(self.wait_for('message',timeout=10.0,check=msg_check))
                await asyncio.sleep(2)
                await rollingchannel.send(roll_prefix)
                try:
                    msg = await wait_for_mudae
                    if msg.content.startswith(f"**{self.user.name}"):
                        
                        wait = get_wait(msg.content)
                        
                except asyncio.TimeoutError:
                    print(f"The Automated rolling on channelid {taskid} is ded. Requires Restart of the program")
                    return
            await asyncio.sleep(wait)
            wait = 0
    
    async def poke_task(self):
        pokechannel = self.get_channel(channelid)
        pokewait = 0
        
        def msg_check(message):
            return message.author.id == mudae and message.channel.id == channelid
        
        while True:
            while pokewait ==0:
                wait_for_poke = self.loop.create_task(self.wait_for('message',timeout=10.0,check=msg_check))
                await asyncio.sleep(2)
                await pokechannel.send("$p")
                try:
                    msgp = await wait_for_poke
                    if "$p:" in msgp.content and "min" in msgp.content:
                        pokewait = get_pwait(msgp.content)
                except asyncio.TimeoutError:
                    print("Poke ded")
                    return
            await asyncio.sleep(pokewait)
            pokewait = 0
                    
client = MyClient()
client.run(token,bot=False)
