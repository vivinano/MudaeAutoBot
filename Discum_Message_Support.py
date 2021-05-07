import discum
import re
import asyncio
import json
import time

jsonf = open("Settings_Mudae.json")
settings = json.load(jsonf)
jsonf.close()

bot = discum.Client(token=settings["token"],log={"console":False, "file":False})
mudae = 432610292342587392

series_list = settings["series_list"]
chars = [charsv.lower() for charsv in settings["namelist"]]
kak_min = settings["min_kak"]
claim_delay = settings["claim_delay"]


kak_finder = re.compile(r'\*\*??([0-9]+)\*\*<:kakera:469835869059153940>')
like_finder = re.compile(r'Likes\: \#??([0-9]+)')
claim_finder = re.compile(r'Claims\: \#??([0-9]+)')


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

@bot.gateway.command
def on_message(resp):
    if resp.event.ready_supplemental:
        global user
        user = bot.gateway.session.user
        
    if resp.event.message:
        m = resp.parsed.auto()
        aId = m['author']['id']
        content = m['content']
        embeds = m['embeds']
        messageid = m['id']
        channelid = m['channel_id']
        #print(f"{messageid} and {channelid}")
        
        if int(aId) == mudae:
            #print("Yes")

            if embeds != []:
                charpop = m['embeds'][0]
                charname = charpop["author"]["name"]
                chardes = charpop["description"]
                charcolor = int(charpop['color'])

                #print(charcolor)

                if str(user['id']) in content:
                    
                    print(f"Wished Sniping")
                    time.sleep(claim_delay)
                    if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                        bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                    else:
                        bot.addReaction(channelid, messageid, "❤")
                
                if charname.lower() in chars:
                    
                    print(f"Char Sniping")
                    time.sleep(claim_delay)
                    if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                        bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                    else:
                        bot.addReaction(channelid, messageid, "❤")
                
                for ser in series_list:
                    if ser in chardes and charcolor == 16751916:
                        
                        
                        print(f"Series Sniping")
                        time.sleep(claim_delay)
                        if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                            bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                            break
                        else:
                            bot.addReaction(channelid, messageid, "❤")
                            break
                            
                if "<:kakera:469835869059153940>" in chardes or ("Claims:" in chardes or "Likes:" in chardes) :
                    kak_value = get_kak(chardes)
                    if int(kak_value) >= kak_min and charcolor == 16751916:
                        
                        
                        print(f"Kakera Value Sniping")
                        time.sleep(claim_delay)
                        if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None:
                            bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                        else:
                            bot.addReaction(channelid, messageid, "❤")
                    
                # if embeds != [] and charcolor == 16751916:
                    # time.sleep(2)
                    
                    # #print(bot.getMessage(channelid, messageid).json()[0]["reactions"][2]["emoji"]['id'])
                    # if "reactions" in bot.getMessage(channelid, messageid).json()[0] and bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]['id'] == None :
                        # bot.addReaction(channelid, messageid, bot.getMessage(channelid, messageid).json()[0]["reactions"][0]["emoji"]["name"])
                    # else:
                        # bot.addReaction(channelid, messageid, "❤")
        
bot.gateway.run()
