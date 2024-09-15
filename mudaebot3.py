import discord
import re
import asyncio
import json
import time
import logging
import threading
from os.path import join as pathjoin
from collections import OrderedDict

class CacheDict(OrderedDict):
    def __init__(self, *args, **kwds):
        self.max = kwds.pop("max", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):
        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):
        if self.max is not None:
            while len(self) > self.max:
                self.popitem(last=False)

msg_buf = CacheDict(max=50)

jsonf = open("Settings_Mudae.json")
settings = json.load(jsonf)
jsonf.close()


mudae = 432610292342587392
use_emoji = "❤️"

with open("cmds.txt","r") as f:
    mudae_cmds = [line.rstrip() for line in f]
mhids = [int(mh) for mh in settings["channel_ids"]]
shids = [int(sh) for sh in settings["slash_ids"]]
ghids = [int(gh) for gh in settings["slash_guild_ids"]]
channel_settings = dict()

series_list = settings["series_list"]
chars = [charsv.lower() for charsv in settings["namelist"]]
kak_min = settings["min_kak"]
roll_prefix = settings["roll_this"]
sniping = settings.get("sniping_enabled",True)


mention_finder = re.compile(r'\<@(?:!)?(\d+)\>')
pagination_finder = re.compile(r'\d+ / \d+')

kak_finder = re.compile(r'\*\*??([0-9]+)\*\*<:kakera:469835869059153940>')
like_finder = re.compile(r'Likes\: \#??([0-9]+)')
claim_finder = re.compile(r'Claims\: \#??([0-9]+)')
poke_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
wait_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min \w')
waitk_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
ser_finder = re.compile(r'.*.')

KakeraVari = [kakerav.lower() for kakerav in settings["emoji_list"]]
#soulLink = ["kakeraR","KakeraO"]
eventlist = ["🕯️","😆"]

#Last min Claims
is_last_enable = True if settings["Last_True"].lower().strip() == "true" else False 
last_claim_window = settings["last_claim_min"]
min_kak_last = settings["min_kak_last_min"]

kakera_wall = {}
waifu_wall = {}

#logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

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


class MyClient(discord.Client):

    async def bg_task(self,taskid):
        rollingchannel = self.get_channel(taskid)
        wait = 0
        def msg_check(message):
            return message.author.id == mudae and message.channel.id == taskid
        
        while True:
            while wait == 0:
                wait_for_mudae = self.loop.create_task(self.wait_for('message',timeout=10.0,check=msg_check))
                await asyncio.sleep(2)
                await rollingchannel.send("$" + roll_prefix)
                try:
                    msg = await wait_for_mudae
                    if msg.content.startswith(f"**{self.user.name}"):
                        
                        wait = get_wait(msg.content)
                        print(wait)
                        
                except asyncio.TimeoutError:
                    print(f"The Automated rolling on channelid {taskid} is ded. Requires Restart of the program")
                    return
            await asyncio.sleep(wait)
            wait = 0

    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        #self.loop.create_task(self.bg_task(807061315792928948))
        

    async def on_message(self, message):
        #Don't Message Self
        if message.author == self.user:
            return
        
        #Interact with Mudae only
        if message.author.id == mudae:
            print("Mudae posted")
            #print(message.guild.id)

            if message.embeds != []:
                objects = message.embeds[0].to_dict()
                #Set up Charname
                if 'author' in objects.keys():
                    charname = objects['author']['name']
                else:
                    charname = "jkqemnxcv not found"
                    
                #Series Sniping
                for ser in series_list:
                    if ser in objects['description'] and objects['color'] == 16751916:               
                        print(f"Attempting to Claim {objects['author']['name']} from {ser} in ({message.channel.id}):{message.channel.name}")
                        emoji = use_emoji
                        await asyncio.sleep(5)
                        if message.components == []:
                            if message.reactions != [] and not message.reactions[0].custom_emoji:
                                emoji = message.reactions[0].emoji
                            await message.add_reaction(emoji)
                            break
                        else:
                            await message.components[0].children[0].click()
                            break
                            
                            
                #Kakera Sniping            
                if message.components != [] and "kakera" in message.components[0].children[0].emoji.name:
                   
                    cooldown = kakera_wall.get(message.guild.id,0) - time.time()
                    if cooldown <= 1:
                        logger.info(f" {message.components[0].children[0].emoji.name} found in: {message.guild.id}")
                        await asyncio.sleep(5)
                        await message.components[0].children[0].click()
                    else:
                        logger.info(f" Skipped {message.components[0].children[0].emoji.name} Skipped in: {message.guild.id}")
                    
                    def kak_check(m):
                        return m.author.id == mudae and m.guild.id == message.guild.id
                        
                    wait_for_kak = self.loop.create_task(self.wait_for('message',timeout=10.0,check=kak_check))
                    try:
                        msgk = await wait_for_kak
                        print(msgk)
                    
                        if msgk.content.startswith(f"**{self.user.name}"):
                            time_to_kak = waitk_finder.findall(msgk.content)
                        else:
                            time_to_kak = []
                        print(time_to_kak)
                        if len(time_to_kak):
                            timegetk = (int(time_to_kak[0][0] or "0")*60+int(time_to_kak[0][1] or "0"))*60
                            logger.info(f"{timegetk} set for server {message.guild.id}")
                            kakera_wall[message.guild.id] = timegetk + time.time()
                    except asyncio.TimeoutError:
                        print("timeout")
                        return

client = MyClient()
client.run(settings['token'])
