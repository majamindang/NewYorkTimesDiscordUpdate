import requests, json, time
from datetime import datetime
from pytz import timezone, utc
from discord_webhook import DiscordWebhook, DiscordEmbed

apiKey = "WanPm29f0UDvTapvGi9CiW9AoVETqg8s"
url = f"https://api.nytimes.com/svc/news/v3/content/all/all.json?api-key={apiKey}"
history = json.loads(open("history.json", 'r').read())

def formatTime(t):
    fmt = '%b %d, %Y | %I:%M:%S %p'
    newT = t.split("T")
    newD = newT[0].split("-")
    newH = newT[1].split("-")[0].split(":")
    dateTime = datetime(int(newD[0]), int(newD[1]), int(newD[2]), int(newH[0]), int(newH[1]), int(newH[2]), tzinfo=utc).strftime(fmt)
    return (dateTime + " ET")

def chooseHook(t):
    # default webhook if chosen keywords not found
    default = "https://discord.com/api/webhooks/914495710404173884/vg82PkT7YAcdzdkns-6thOqQgpzR--c_5eDSELAv5jTX1BIlhUb5hVicCy5tpZSRQji8"
    
    # choose hook by keywords
    options = [
        {
            "keywords":[
                "Breaking:",
                "Important:"
            ],

            "hook": "https://discord.com/api/webhooks/914495710404173884/vg82PkT7YAcdzdkns-6thOqQgpzR--c_5eDSELAv5jTX1BIlhUb5hVicCy5tpZSRQji8"
        }
    ]

    for i in options:
        for y in i['keywords']:
            if(y.lower() in t.lower()):
                return i['hook']

    return default

with open("logs.txt", "a") as o:
    print('Waiting for new articles ...')
    while True: 
        r = json.loads(requests.get(url).text)
        for i in r['results']:
            if((i['slug_name'] + i['updated_date'] not in history)):
                updated = ""
                up = ""
                history.append(i["slug_name"] + i['updated_date'])
                if(i['published_date'] != i['updated_date']):
                    updated = f'\nUpdated: {formatTime(i["updated_date"])}'
                    up = " [UPDATED]"
                webhook = DiscordWebhook(url=chooseHook(i['title']))
                embed = DiscordEmbed(title=i['title'] + up, description=f"{i['abstract']}\n\n{i['byline']}\nURL: {i['url']}\nPublished: {formatTime(i['published_date'])} {updated}", color='03b2f8')

                try:
                    embed.set_thumbnail(url=i['thumbnail_standard'])
                except:
                    pass

                webhook.add_embed(embed)
                response = webhook.execute()
                print(i['slug_name'] + " sent to discord!")

        o = open("history.json", 'w')
        o.write(json.dumps(history, indent=4))
        o.close()
        time.sleep(10)