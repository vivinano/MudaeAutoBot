import discord
import asyncio
import re
import json


jsonf = open("Settings_Mudae.json")
settings = json.load(jsonf)
jsonf.close()


#Settings
token = settings["token"]
mudae = 432610292342587392
channelid = settings["channel_id"]
claim_delay = settings["claim_delay"]
kak_delay = settings["kak_delay"]
roll_prefix = settings["roll_this"]
kak_min = settings["min_kak"]

wait_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min left')
kak_finder = re.compile(r'\*\*??([0-9]+)\*\*<:kakera:469835869059153940>')
like_finder = re.compile(r'Likes\: \#??([0-9]+)')
claim_finder = re.compile(r'Claims\: \#??([0-9]+)')
poke_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
#use_emoji = settings["use_emoji"]
use_emoji = "❤️"


series_list = settings["series_list"]
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
            await asyncio.sleep(6)
            self.loop.create_task(self.bg_task())
        
        
            

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
           return

        
        if message.author.id == mudae:
            print(message.content)
                             
            if message.embeds != []:
                objects = message.embeds[0].to_dict()
                print(objects['author'])
                
                
                for ser in series_list:
                    if ser in objects['description'] or str(self.user.id) in message.content:               
                        #print(objects['description'])
                        emoji = use_emoji
                        await asyncio.sleep(claim_delay)
                        await message.add_reaction(emoji)
                        break
                        
                if "<:kakera:469835869059153940>" in objects['description'] or ("Claims:" in objects['description'] or "Likes:" in objects['description']) :
                    kak_value = get_kak(objects['description'])
                    print(kak_value)
                    if int(kak_value) >= kak_min and ("**$togglereact**" in objects['description'] or objects['color'] == 16751916):
                        emoji = use_emoji
                        await asyncio.sleep(claim_delay)
                        await message.add_reaction(emoji)
                        print("Possible Claim")
                        
                    
    

    async def on_reaction_add(self,reaction,user):
        if(reaction.custom_emoji and reaction.emoji.name.lower() in KakeraVari):
            await asyncio.sleep(kak_delay)
            await reaction.message.add_reaction(reaction.emoji)
                
                
        
        if (user.id == mudae and not reaction.custom_emoji):
            if reaction.emoji in eventlist:
                await asyncio.sleep(kak_delay)
                await reaction.message.add_reaction(reaction.emoji)
                
            
            
    async def bg_task(self):
        rollingchannel = self.get_channel(channelid)
        wait = 0
        def msg_check(message):
            return message.author.id == mudae and message.channel.id == channelid
        
        while True:
            while wait == 0:
                wait_for_mudae = self.loop.create_task(self.wait_for('message',timeout=10.0,check=msg_check))
                await asyncio.sleep(2)
                await rollingchannel.send(roll_prefix)
                try:
                    msg = await wait_for_mudae
                    if msg.content.startswith(f"**{self.user.name}") and "min" in msg.content:
                        
                        wait = get_wait(msg.content)
                        
                except asyncio.TimeoutError:
                    print(f"mudae ded.")
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
                await asyncio.sleep(4)
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
