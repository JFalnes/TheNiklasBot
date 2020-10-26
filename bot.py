# Author:       F4lnes
# Created:      09.04.2020

# Niklas-Bot Source Code
# If found, return to owner
import asyncio
import shutil
import threading
import time
import youtube_dl as youtube_dl
import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import praw
import pyjokes
import requests
import json
from gtts import gTTS

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')

# change this variable to whatever your download folder for the bot will be
folder = r'/home/pi/Desktop/Niklas-Bot/NiklasDL'
# change this variable to your ffmpeg installation directory
ffmpeg_ex = r'C:\ffmpeg\bin\ffmpeg.exe'
PREFIX = '!'
VERSION = '1.0'
CHANGELOG = f'Version {VERSION} contains multiple bugfixes, QoL changes and some new features:\n' \
            f'1. !gamble, start a betting match with your friends! \n' \
            f'2. !clean, for administrators. Keep your discord neat and tidy!\n' \
            f'As always, every version contains multiple bugfixes to make Niklas work harder to please you'

bot = commands.Bot(command_prefix='!')

client = discord.Client()

r = praw.Reddit(client_id=REDDIT_ID,
                client_secret=REDDIT_SECRET,
                user_agent='<console:myFirstBot:1.0 (by /u/user)>', username='', password="")

list_of_stealing = ['aggressively stolen from', 'willfully given to Niklas by', 'forcefully taken from',
                    'confiscated from', 'confiscated, for the good of the realm from']

sub_list = ['memes', 'blackpeopletwitter', 'whitepeopletwitter', 'meirl', 'WholesomeMemes',
            'prequelmemes', 'lotrmemes', 'historymemes', 'comedycemetery', 'comedyheaven']


def reddit_meme():
    s = random.choice(sub_list)
    sub = r.subreddit(s)

    for a in sub.hot(limit=20):
        random_post_number = random.randint(2, 25)
        for i, posts in enumerate(sub.hot(limit=20)):
            if i == random_post_number:
                return f'Title: **{posts.title}**\n' \
                       f'{posts.url} \n' \
                       f' {random.choice(list_of_stealing)} _/r/{sub}_'


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': f'{folder}/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


def delete_DL():
    while True:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            print('Cleaned')
            time.sleep(900)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(source=filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(description='Test')
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source=query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def sb(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source=query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def text(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        tts = gTTS(text=query, lang='en')
        tts.save('tts.mp3')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source='tts.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def textjoke(self, ctx):
        """Plays a file from the local filesystem"""
        joke = pyjokes.get_joke()

        tts = gTTS(text=joke, lang='en')
        tts.save('textjoke.mp3')
        query = 'textjoke.mp3'
        # CHANGE THE EXECUTABLE TO YOUR FFMPEG DIRECTORY
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source=query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def yt(self, ctx, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                         source=player))
            ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stream(self, ctx, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    @text.before_invoke
    @sb.before_invoke
    @textjoke.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Sends a random meme')
    async def meme(self, ctx):
        print('Works')
        await ctx.send(reddit_meme())


class Funny(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(description='Sends a random joke, uses PyJokes Library')
    async def joke(self, ctx):
        await ctx.send(pyjokes.get_joke())

    @commands.command(description='Who is up for a gamble?')
    async def gamble(self, ctx):
        await ctx.send('Alright everyone, place your bets! Pick a number between 1-10 and whoever gets it right wins')
        time.sleep(2)
        await ctx.send('8 seconds left!')
        time.sleep(2)
        await ctx.send('6 seconds left!')
        time.sleep(2)
        await ctx.send('4 seconds left!')
        time.sleep(2)
        await ctx.send('2 seconds left!')
        time.sleep(1)
        await ctx.send('1 seconds left!')
        time.sleep(1)
        await ctx.send(f'The correct number was {random.choice(range(1, 10))}')


class dnd(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def d2(self, ctx):
        diceroll = random.randint(1, 2)
        await ctx.send(diceroll)

    @commands.command()
    async def d4(self, ctx):
        diceroll = random.randint(1, 4)
        await ctx.send(diceroll)

    @commands.command()
    async def d6(self, ctx):
        diceroll = random.randint(1, 6)
        await ctx.send(diceroll)

    @commands.command()
    async def d8(self, ctx):
        diceroll = random.randint(1, 8)
        await ctx.send(diceroll)

    @commands.command(aliases=['dndice 10'])
    async def d10(self, ctx):
        diceroll = random.randint(1, 10)
        await ctx.send(diceroll)

    @commands.command()
    async def d12(self, ctx):
        diceroll = random.randint(1, 12)
        await ctx.send(diceroll)

    @commands.command()
    async def d20(self, ctx):
        diceroll = random.randint(1, 20)
        await ctx.send(diceroll)


class misc(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def changelog(self, ctx):
        await ctx.send(CHANGELOG)

    @bot.command(description='Cleans the chat')
    @commands.has_permissions(administrator=True)
    async def clean(self, ctx, limit: int):

        await ctx.message.channel.purge(limit=limit)
        await ctx.channel.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

    @clean.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("You cant do that!")

    @commands.command()
    async def slap(self, ctx):
        try:
            user = ctx.message.mentions[0]

            await ctx.send(f'{user.mention} HOWS IT FEEL GETTING SLAPPED\n '
                           f'https://tenor.com/view/amanda-bynes-slap-gif-4079563')
        except:
            author = ctx.message.author
            await ctx.send(f'{author.mention} YOU GOTTA DO !SLAP @USERNAME YOU\n '
                           f'https://tenor.com/view/amanda-bynes-slap-gif-4079563')

    @commands.command()
    async def covid(self, ctx):
        a = requests.get('https://api.covid19api.com/summary')
        p = json.loads(a.text)
        s = json.dumps(p)

        for k, v in p.items():
            loc = 'Global'
            if k == loc:
                stats = (f'Coronavirus Statistics for {loc}: \n' +
                         'Total Cases: ' + str(v['TotalConfirmed']) + '\n' +
                         'New Cases: ' + str(v['NewConfirmed']) + '\n' +
                         'Total Deaths: ' + str(v['TotalDeaths']) + '\n' +
                         'New Deaths: ' + str(v['NewDeaths']) + '\n' +
                         'Data Collected from https://covid19api.com/\n' + 'Stay Safe'
                         )
                await ctx.send(stats)

    @commands.command()
    async def week(self, ctx):
        a = requests.get('http://ukenummer.no/json')
        p = json.loads(a.text)
        s = json.dumps(p, indent=2, sort_keys=True)

        for k, v in p.items():

            if k == 'weekno':
                weekno = str(v)
            if k == 'dates':
                await ctx.send(
                    f'It is currently week {weekno}, which lasts from {str(v["fromdate"])} to {str(v["todate"])}.')


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Your friendly neighbourhood Niklas')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    activity = discord.Game(name=f"!help, version {VERSION}")
    await bot.change_presence(status=discord.Status.online, activity=activity)


t1 = threading.Thread(target=delete_DL)
t1.start()
bot.add_cog(dnd(bot))

bot.add_cog(misc(bot))
bot.add_cog(Funny(bot))
bot.add_cog(Reddit(bot))
bot.add_cog(Music(bot))
bot.run(TOKEN)
