import discum
import re
import asyncio
import json
import time
import logging
import threading

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

bot = discum.Client(token=settings["token"],log={"console":False, "file":False})
mudae = 432610292342587392
with open("cmds.txt","r") as f:
    mudae_cmds = [line.rstrip() for line in f]
mhids = [int(mh) for mh in settings["channel_ids"]]
channel_settings = dict()

series_list = settings["series_list"]
chars = [charsv.lower() for charsv in settings["namelist"]]
kak_min = settings["min_kak"]
roll_prefix = settings["roll_this"]
sniping = settings.get("sniping_enabled",True)

ready = False

mention_finder = re.compile(r'\<@!(\d+)\>')
pagination_finder = re.compile(r'\d+ / \d+')

kak_finder = re.compile(r'\*\*??([0-9]+)\*\*<:kakera:469835869059153940>')
like_finder = re.compile(r'Likes\: \#??([0-9]+)')
claim_finder = re.compile(r'Claims\: \#??([0-9]+)')
poke_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
wait_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min \w')
waitk_finder = re.compile(r'\*\*(?:([0-9+])h )?([0-9]+)\*\* min')
ser_finder = re.compile(r'.*.')

KakeraVari = [kakerav.lower() for kakerav in settings["emoji_list"]]
eventlist = ["🕯️","😆"]


kakera_wall = {}
waifu_wall = {}

#logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

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
def get_serial(text):
    serk = ser_finder.findall(text)
    return serk[0]

_resp = dict()
def wait_for(bot, predicate, timeout=None):
    ev = threading.Event()
    ident = threading.get_ident()
    def evt_check(resp):
        if predicate(resp):
            _resp[ident] = resp.parsed.auto()
            ev.set()
    bot.gateway._after_message_hooks.insert(0,evt_check)
    ev.wait(timeout)
    bot.gateway.removeCommand(evt_check)
    obj = _resp.pop(ident,None)
    
    return obj

def mudae_warning(tide,StartwithUser=True):
    # build check func
    def c(r):
        if r.event.message:
            r = r.parsed.auto()
            # must be from relevant channel id, and start with username
            if StartwithUser == True:
                return r['author']['id'] == str(mudae) and r['channel_id'] == tide and r['content'].startswith(f"**{bot.gateway.session.user['username']}")
            elif StartwithUser == False:
                return r['author']['id'] == str(mudae) and r['channel_id'] == tide
        return False
    return c

def get_server_settings(guild_id,channel_id):
    msgs = bot.searchMessages(guild_id,userID=[mudae],textSearch="($togglehentai)").json()['messages']

    for group in msgs:
        for result in group:
            if 'hit' in result:
                if result['content'].startswith("🛠️"):
                    return result['content']
    
    # no setting found
    # so send settings request, and hope they have default prefix.
    bot.sendMessage(channel_id,"$settings")
    def checker(r):
        if r.event.message: 
            r = r.parsed.auto()
            return r['channel_id'] == channel_id and r['author']['id'] == str(mudae) and r['content'].startswith("🛠️")
        return False
    m = wait_for(bot,checker,timeout=5)
    if m == None:
        return None
    return m.get('content')

def parse_settings_message(message):
    if message == None:
        return None
    val_parse = re.compile(r'\*\*(\S+)\*\*').findall
    num_parse = re.compile(r'(\d+)').findall

    settings_p = re.findall(r'\w+: (.*)',message)
    settings = dict()

    settings['prefix'] = val_parse(settings_p[0])[0]
    settings['prefix_len'] = len(settings['prefix'])
    settings['claim_reset'] = int(num_parse(settings_p[2])[0]) # in minutes
    settings['reset_min'] = int(num_parse(settings_p[3])[0])
    settings['shift'] = int(num_parse(settings_p[4])[0])
    settings['max_rolls'] = int(num_parse(settings_p[5])[0])
    settings['expiry'] = float(num_parse(settings_p[6])[0])
    settings['claim_snipe'] = [float(v) for v in num_parse(settings_p[15])]
    settings['kak_snipe'] = [float(v) for v in num_parse(settings_p[16])]

    settings['claim_snipe'][0] = int(settings['claim_snipe'][0])
    # pad out claim/kak snipe for default '0 second cooldown'
    if len(settings['claim_snipe']) < 2:
        settings['claim_snipe'] += [0.0]
    if len(settings['kak_snipe']) < 2:
        settings['kak_snipe'] += [0.0]
    settings['claim_snipe'][0] = int(settings['claim_snipe'][0])
    settings['kak_snipe'][0] = int(settings['kak_snipe'][0])

    settings['pending'] = None
    settings['rolls'] = 0

    return settings

def get_snipe_time(channel,rolled,message):
    # Returns delay for when you are able to snipe a given roll
    r,d = channel_settings[channel]['claim_snipe']
    if r == 0:
        # Anarchy FTW!
        return 0.0
    
    global user
    if (r < 4 or r == 5) and rolled == user['id']:
        # Roller can insta-snipe.
        return 0.0
    
    wished_for = mention_finder.findall(message)
    if not len(wished_for) and r == 3 or r == 4:
        # Not a WISHED character, insta-snipe possible
        return 0.0
    if r > 2 and user['id'] in wished_for:
        # Wisher can insta-snipe
        return 0.0
    elif r == 1 and rolled not in wished_for:
        # Roller (who is not us) did not wish for char, so can insta-snipe
        return 0.0
    return d

def next_claim(channel):
    channel = int(channel)
    offset = (120-(channel_settings[channel]['shift']+channel_settings[channel]['reset_min']))*60
    
    reset_period = channel_settings[channel]['claim_reset']*60
    t = time.time()+offset
    last_reset = (t%86400)%reset_period
    reset_at = reset_period-last_reset+time.time()

    return (int(t/reset_period),reset_at) # claim window id, timestamp of reset

def next_reset(channel):
    # Returns timestamp of next reset
    channel = int(channel)
    offset = channel_settings[channel]['reset_min']*60
    t = time.time()
    return t+(3600-((t-offset)%3600))

def poke_roll(tide):
    logger.debug(f"Pokemon Rolling Started in channel {tide}. (If you would like this in a different channel, please configure the desired channel ID as the first in your list)")
    tides = str(tide)
    if tide not in channel_settings:
        logger.error(f"Could not find channel {tide}, will not roll poke")
        return
    c_settings = channel_settings[tide]
    pwait = 0
    while True:
        while pwait == 0:
            time.sleep(2)
            bot.sendMessage(tides,c_settings['prefix']+"p")
            pwait = 2*60*60 # sleep for 2 hours
        print(f"{pwait} : pokerolling : {tide}")
        time.sleep(pwait) 
        pwait = 0

def waifu_roll(tide):
    logger.debug(f"waifu rolling Started in channel {tide}")
    tides = str(tide)
    waifuwait = 0

    if tide not in channel_settings:
        logger.error(f"Could not find channel {tide}, skipping waifu roll on this channel.")
        return
    c_settings = channel_settings[tide]
    roll_cmd = "$" + roll_prefix
    if c_settings:
        roll_cmd = c_settings['prefix'] + roll_prefix
    while True:
        c_settings['rolls'] = 0
        while waifuwait == 0:
            bot.sendMessage(tides,roll_cmd)
            
            varwait = wait_for(bot,mudae_warning(tides,False),timeout=5)
            time.sleep(.5)
            
            if varwait != None and varwait['content'].startswith(f"**{bot.gateway.session.user['username']}"):
                waifuwait = next_reset(tide)-time.time()
            elif c_settings['rolls'] >= c_settings['max_rolls']:
                waifuwait = next_reset(tide)-time.time()
        print(f"{waifuwait}: Waifu rolling : {tide}")
        time.sleep(waifuwait)
        waifuwait = 0

def snipe(recv_time,snipe_delay):
    if snipe_delay == 0.0:
        return
    try:
        time.sleep((recv_time+snipe_delay)-time.time())
    except ValueError:
        # sleep was negative, so we're overdue!
        return
    time.sleep(.5)

@bot.gateway.command
def on_message(resp):
    global user
    recv = time.time()
    if resp.event.message:
        m = resp.parsed.auto()
        #print(m)
        aId = m['author']['id']
        content = m['content']
        embeds = m['embeds']
        messageid = m['id']
        channelid = m['channel_id']
        guildid = m['guild_id']

        if int(channelid) not in mhids:
            # Not a channel we work in.
            return
        
        if int(channelid) not in channel_settings:
            mhids.remove(int(channelid))
            logger.error(f"Could not find settings for {channelid}, please trigger the '$settings' command in the server and run the bot again.")
            return
        c_settings = channel_settings[int(channelid)]

        if c_settings['pending'] == None and int(aId) != mudae and content[0:c_settings['prefix_len']] == c_settings['prefix'] and content.split(' ')[0][c_settings['prefix_len']:] in mudae_cmds:
            # Note rolls as they happen so we know who rolled what
            c_settings['pending'] = aId
            return
        
        elif int(aId) == mudae:
            roller = c_settings['pending']
            c_settings['pending'] = None
            # Validate this is a rolled character.
            if len(embeds) != 1 or "image" not in embeds[0] or "author" not in embeds[0] or list(embeds[0]["author"].keys()) != ['name']:
                # not a marry roll.
                return
            elif 'footer' in embeds[0] and 'text' in embeds[0]['footer'] and len(pagination_finder.findall(embeds[0]['footer']['text'])):
                # Has pagination e.g. "1 / 29", which does not occur when rolling
                return
            msg_buf[messageid] = roller == user['id']
            print("Our user rolled" if roller == user['id'] else "Someone else rolled")
            
            if "interaction" in m:
                # Mudae triggered via slash command
                roller = m['interaction']['user']['id']
            
            if(not sniping and roller != user['id']):
                # Sniping disabled by user
                return
            
            if roller == user['id']:
                # confirmed user roll
                c_settings['rolls'] += 1
            
            if waifu_wall.get(channelid,0) != next_claim(channelid)[0]:
                snipe_delay = get_snipe_time(int(channelid),roller,content)
                charpop = m['embeds'][0]
                charname = charpop["author"]["name"]
                chardes = charpop["description"]
                charcolor = int(charpop['color'])

                #print(charcolor)

                if str(user['id']) in content:
                    logger.info(f"Wished {charname} from {get_serial(chardes)} with {get_kak(chardes)} Value in Server id:{guildid}")
                    snipe(recv,snipe_delay)
                    if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                        bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                    else:
                        bot.addReaction(channelid, messageid, "❤")
                
                if charname.lower() in chars:
                    
                    logger.info(f"{charname} appeared attempting to Snipe Server id:{guildid}")
                    snipe(recv,snipe_delay)
                    
                    if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                        bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                    else:
                        bot.addReaction(channelid, messageid, "❤")
                
                for ser in series_list:
                    if ser in chardes and charcolor == 16751916:
                        
                        
                        logger.info(f"{charname} from {ser} appeared attempting to snipe in {guildid}")
                        snipe(recv,snipe_delay)
                        if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                            bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                            break
                        else:
                            bot.addReaction(channelid, messageid, "❤")
                            break

                if "<:kakera:469835869059153940>" in chardes or "Claims:" in chardes or "Likes:" in chardes:
                    kak_value = get_kak(chardes)
                    if int(kak_value) >= kak_min and charcolor == 16751916:
                        
                        
                        logger.info(f"{charname} with a {kak_value} Kakera Value appeared Server:{guildid}")
                        snipe(recv,snipe_delay)
                        if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                            bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                        else:
                            bot.addReaction(channelid, messageid, "❤")
                
                if str(user['id']) not in content and charname.lower() not in chars and get_serial(chardes) not in series_list and int(get_kak(chardes)) < kak_min:
                    logger.debug(f"Ignoring {charname} from {get_serial(chardes)} with {get_kak(chardes)} Kakera Value in Server id:{guildid}")
                    
    if resp.event.message_updated:
        # Handle claims
        r = resp.parsed.auto()
        rchannelid = r["channel_id"]
        try:
            if r['author']['id'] == str(mudae):
                for embed in r['embeds']:
                    f = embed.get('footer')
                    if f and bot.gateway.session.user['username'] in f['text']:
                        # Successful claim, mark waifu claim window as used
                        waifu_wall[rchannelid] = next_claim(rchannelid)[0]
        except KeyError as e:
            pass

    if resp.event.reaction_added:
        r = resp.parsed.auto()
        #print(r)
        reactionid = int(r['user_id'])
        rchannelid = r["channel_id"]
        rmessageid = r["message_id"]
        rguildid = r["guild_id"]
        emoji = r["emoji"]["name"]
        emojiid = r["emoji"]['id']

        if int(rchannelid) not in mhids:
            # Not a channel we work in.
            return
        
        if int(rchannelid) not in channel_settings:
            mhids.remove(int(rchannelid))
            logger.error(f"Could not find settings for {rchannelid}, please trigger the '$settings' command in the server and run the bot again.")
            return

        snipe_delay = channel_settings[int(rchannelid)]['kak_snipe'][1]
        
        if reactionid == mudae and int(rchannelid) in mhids:
            
            if emojiid != None and emoji == "kakeraP" and (snipe_delay == 0 or msg_buf[rmessageid]):
                sendEmoji = emoji + ":" +emojiid
                react_m = bot.getMessage(rchannelid, rmessageid).json()[0]['embeds'][0]
                time.sleep(1)
                bot.addReaction(rchannelid,rmessageid,sendEmoji)
                
            if emojiid != None and emoji.lower() in KakeraVari:
                sendEmoji = emoji + ":" +emojiid
                react_m = bot.getMessage(rchannelid, rmessageid).json()[0]['embeds'][0]
                
                claim_window = next_claim(rchannelid)[0]
                on_cooldown = kakera_wall.get(rchannelid,0) == claim_window
                if not on_cooldown:
                    logger.info(f"{emoji} was detected on {react_m['author']['name']}:{get_serial(react_m['description'])} in Server: {rguildid}")
                    time.sleep(snipe_delay)
                    bot.addReaction(rchannelid,rmessageid,sendEmoji)
                    kakera_wall[rchannelid] = claim_window
                else:
                    logger.info(f"Skipped {emoji} found on {react_m['author']['name']}:{get_serial(react_m['description'])} in Server: {rguildid}")
                    return 

                warn_check = mudae_warning(rchannelid)
                kakerawallwait = wait_for(bot,lambda r: warn_check(r) and 'kakera' in r.parsed.auto()['content'],timeout=5)

                if kakerawallwait != None:
                    time_to_wait = waitk_finder.findall(kakerawallwait['content'])
                else:
                    time_to_wait = []
                
                if len(time_to_wait):
                    kakera_wall[rchannelid] = claim_window
            
            if emojiid == None:
                if emoji in eventlist:
                    print(f"{emoji} was detected in Server: {rguildid}")
                    time.sleep(snipe_delay)
                    bot.addReaction(rchannelid,rmessageid,emoji)

    global ready
    if resp.event.ready_supplemental and not ready:
        ready = True
        user = bot.gateway.session.user

        guilds = bot.gateway.session.settings_ready['guilds']
        chs = set(str(mhid) for mhid in mhids)
        for gid, guild in guilds.items():
            for matched_channel in (set(guild['channels'].keys()) & chs):
                # Find associated guild ID to a monitored channel, then get settings
                msg = get_server_settings(gid,matched_channel)
                c_settings = parse_settings_message(msg)
                channel_settings[int(matched_channel)] = c_settings
        
        if settings['pkmrolling'].lower().strip() == "true":
            p = threading.Thread(target=poke_roll,args=[mhids[0]])
            p.start()
        if settings['rolling'].lower().strip() == "true":
            for chid in mhids:
                waifus = threading.Timer(10.0,waifu_roll,args=[chid])
                waifus.start()

def empty(*args,**kwargs):
    return

#bot.sendMessage = empty


bot.gateway.run(auto_reconnect=True)
