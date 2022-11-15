# -*- coding: utf-8 -*-

import os
import shutil
import random
import discord
from discord.ext import commands
import yt_dlp
import urllib.request
import urllib.parse
import re
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='Рыжий ', intents=intents)

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessor': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodac': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': './Загрузка/%(title)s.%(ext)s',
}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect.delay_max 5',
                  'options': '-vs'}
Mats = ['бля', 'бля буду', 'блядь', 'блядство', 'ебать', 'ебало', 'ебало', 'ебальник', 'ебать его в рот', 'ебать его конем', 'ебать колотить', 'ебать мой рот', 'ебаться сраться', 'ебическая сила', 'ебло', 'еблом по щелкай', 'поебать', 'шобла ебла', 'не выебывайся', 'долбоеб', 'ебанатик', 'дуроеб', 'ебанутый', 'ебаришка', 'ебать копать', 'ебливая ты сука', 'ебукентий', 'ебарь', 'ебнутый', 'ебеня матерь', 'ебантроп', 'ебанатический', 'еблище', 'ебицкая сила', 'невротебательский', 'уебан', 'уебантус', 'заеб', 'злоебучий ты мудак', 'изъебнись', 'к ебеням нахуй', 'коноебится', 'мозгоеб', 'мудоеб', 'разъебай', 'худоебина', 'взъебка', 'доебаться', 'ебаторий', 'ебать мозги', 'ебаться тебе только с рукой', 'ебля']
Queue = []
QName = []
id_bot_chat = ''
conn = False
loop = False
q = 0

def clearing():
    print('Чистим файлы')
    for f in os.listdir('./Музыка'):
        os.remove(os.path.join('./Музыка', f))
    for f in os.listdir('./Загрузка'):
        os.remove(os.path.join('./Загрузка', f))
    Queue.clear()
    return 0

def Q(ctx):
    global q, loop
    print(f'Номер песни равен: ', (q+1))
    try:
        if q <= len(Queue)-1:
            if ctx.message.guild.voice_client.is_playing() is False:
                play(ctx)
                print('Следующая песня')
            return 0
        elif loop:
            q = 0
            Q(ctx)
            print('Цикл обновлен')
        elif ctx.message.guild.voice_client.is_playing() is False:
            q = 0
            print('Конец списка')
            return 0
    except AttributeError:
        print('Бот отключен')


def play(ctx):
    global q
    ctx.guild.voice_client.play(discord.FFmpegPCMAudio(executable='C:\\FFmpeg\\ffmpeg.exe', source='.\Музыка//'+Queue[q]), after=lambda x: Q(ctx))
    print('Играю музыку')
    q = q + 1
    return 0

def disconnect():
    global conn, loop, q, id_bot_chat
    conn = False
    loop = False
    id_bot_chat = ''
    q = 0

@bot.event
async def on_ready():
    clearing()
    print('Я жив!')

@bot.event
async def on_voice_state_update(member, before, after):
    if not member.id == bot.user.id:
        return
    elif before.channel is None:
        voice = after.channel.guild.voice_client
        time = 0
        while True:
            await asyncio.sleep(1)
            time = time + 1
            if voice.is_playing() and not voice.is_paused():
                time = 0
            if time == 10:
                await voice.disconnect()
            if not voice.is_connected():
                break
    elif member == bot.user:
        disconnect()
        clearing()
        print('Бот отключен')

@bot.command()
async def матерись(ctx):
    await ctx.send(Mats[random.randint(0, 51)])

@bot.command(name="монетка", help="Бросает монетку")
async def монетка(ctx):
    x = random.randint(0, 1)
    if x == 0:
        await ctx.send('Орёл!')
    else:
        await ctx.send('Решка!')
    print(bot.get_channel())

@bot.command(name="куб", help="Бросает куб с вашим количеством граней")
async def куб(ctx, *, text):
    x = int(text)
    rand = random.randint(1, x)
    await ctx.send(f'Результат броска: {rand}')

@bot.command(help="Повторяет музыку из списка")
async def повторяй(ctx):
    global loop
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    loop = True
    print('Музыка зациклена')
    await ctx.send('Теперь музыка на повторе')

@bot.command(name="не повторяй", help="Прекращает повторять музыку")
async def не(ctx, word):
    global loop
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    if word == 'повторяй':
        loop = False
        print('Музыка больше не зациклена')
        await ctx.send('повторение музыки прекращено')

@bot.command(help="Приостанавливает проигрывание музыки")
async def остановись(ctx):
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    if ctx.message.guild.voice_client.is_playing():
        ctx.message.guild.voice_client.pause()
        print('Музыка на паузе')

@bot.command(help="Продолжает воспроизведение музыки")
async def продолжай(ctx):
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    if ctx.message.guild.voice_client.is_paused():
        ctx.message.guild.voice_client.resume()
        print('Музыка продолжается')

@bot.command(help="Отключается из чата")
async def отключись(ctx):
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    if conn:
        print('Отключение через чат')
        await ctx.message.guild.voice_client.disconnect()

@bot.command(help="Пропускает песню из списка")
async def пропусти(ctx):
    global q
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    print('Пропускаю песню')
    if ctx.message.guild.voice_client.is_playing():
        ctx.message.guild.voice_client.stop()
        if q < len(Queue)-1 or loop:
            Q(ctx)
        else:
            await ctx.message.guild.voice_client.disconnect()


@bot.command(help="Удаляет песню из списка")
async def удали(ctx):
    global q
    if ctx.author.voice.chanell != id_bot_chat:
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0
    print('Удаляю песню')
    if ctx.message.guild.voice_client.is_playing():
        ctx.message.guild.voice_client.stop()
        dir = './Музыка/'+Q[q]
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        if q < len(Queue) - 1 or loop:
            Q(ctx)
        else:
            await ctx.message.guild.voice_client.disconnect()

@bot.command(pass_context=True, help="Проигрывает музыку по названию или ссылке из YouTube.  Пример: Рыжий играй {Название песни}")
async def играй(ctx, *, url: str):
    global q, conn, id_bot_chat
    connected = ctx.author.voice
    if conn is False:
        if connected:
            conn = True
            await connected.channel.connect()
        else:
            await ctx.send('Вы не подключены к какому либо голосовому чату!')
            return 0
    if connected.channel != id_bot_chat and id_bot_chat != '':
        await ctx.send('Вы не подключены к используемуму голосовому чату!')
        return 0

    id_bot_chat = connected.channel

    if url.startswith('https') is False:
        search = 'https://www.youtube.com/results?search_query=' + urllib.parse.quote_plus(url)
        html = urllib.request.urlopen(search)
        url = 'https://www.youtube.com/watch?v=' + re.findall(r'watch\?v=(\S{11})', html.read().decode())[0]


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

        print('новое скачал')

        for file in os.listdir('./Загрузка/'):
            if file.endswith('.webm'):
                print(file)
                Queue.append(file)
                try:
                    shutil.move('./Загрузка/'+file, './Музыка')
                except:
                    os.remove(file)
                    print('Уже скачано')
                print('Переименовал')
        if not ctx.message.guild.voice_client.is_playing():
            play(ctx)
        i = 0
        name = ''
        while file[i] != '.':
            name = name + file[i]
            i = i + 1
        await ctx.send(f'В список добавлена: {name}')

bot.run('MTAwMDYzNTcxODA2MzkwMjc0MQ.GCGBOB.qGdwAtkdH7ODOEQDAVmNihrDTW0sa5zWOevIdg')