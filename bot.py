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
# change these variables in your .env file to point to the right tokens or paths
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
REDDIT_ID = os.getenv('REDDIT_ID')
REDDIT_SECRET = os.getenv('REDDIT_SECRET')
FOLDER_PATH = os.getenv('FOLDER_PATH')
FFMPEG_PATH = os.getenv('FFMPEG_PATH')

folder = FOLDER_PATH
ffmpeg_ex = FFMPEG_PATH
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

# phrases the bot will say when posting a meme from reddit, change as you want
list_of_stealing = ['aggressively stolen from', 'willfully given to Niklas by', 'forcefully taken from',
                    'confiscated from', 'confiscated, for the good of the realm from']

# change or update this list to what you want
sub_list = ['memes', 'blackpeopletwitter', 'whitepeopletwitter', 'meirl', 'WholesomeMemes',
            'prequelmemes', 'lotrmemes', 'historymemes', 'comedycemetery', 'comedyheaven']

list_of_ball = ['As I see it, yes', 'Ask again later.', 'Better not tell you now.', ' Cannot predict now.',
                'Concentrate and ask again.', 'Don’t count on it.', 'It is certain.', 'It is certain.',
                'It is decidedly so.', 'Most Likely.', 'My reply is no.', 'My sources say no.',
                'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.',
                'Very doubtful.', ' Without a doubt.', 'Yes.', 'Yes - definitely', 'You may rely on it.']


def eight_answer():
    response = random.choice(list_of_ball)
    return ':8ball:, ' + response


def poke_api(msg):
    """uses pokepy and pokeapi
    https://pokeapi.github.io/pokepy/"""
    try:
        pokemon_name = pokepy.V2Client().get_pokemon(msg)

        response = f'Name: {pokemon_name.name}\n' \
                   f'Weight: {pokemon_name.weight}\n' \
                   f'Type: {pokemon_name.types[0].type.name}'
        return response
    except:
        error_code = f'{msg} IS NOT A POKEMON'
        return error_code


def week_api():
    a = requests.get('http://ukenummer.no/json')
    p = json.loads(a.text)
    s = json.dumps(p, indent=2, sort_keys=True)

    for k, v in p.items():

        if k == 'weekno':
            weekno = str(v)
        if k == 'dates':
            return f'It is currently week {weekno}, which lasts from {str(v["fromdate"])} to {str(v["todate"])}.'


def covid_api():
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
            return stats


# function for retrieving posts from reddit
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


def facts():
    URL = 'https://uselessfacts.jsph.pl/random.json?language=en'

    r = requests.get(URL).json()
    for key, value in r.items():
        if key == 'text':
            fact = f'{value}\n' \
                   f'Facts collected from https://uselessfacts.jsph.pl/ !'
            return fact


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
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


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
        """Text to speech, output in channel user is in"""
        tts = gTTS(text=query, lang='en')
        tts.save('tts.mp3')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_ex,
                                                                     source='tts.mp3'))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

    @commands.command()
    async def textjoke(self, ctx):
        """Uses pyjokes library to create a text to speech file, and plays in channel user is in"""
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
        await ctx.send(reddit_meme())


class Funny(commands.Cog):
    def __init(self, bot):
        self.bot = bot

    @commands.command()
    async def pokemon(self, ctx):
        content = ctx.message.content
        a = content.split(' ', 1)
        msg = a[1]
        await ctx.send(poke_api(msg))

    @commands.command(description='Sends a random joke, uses PyJokes Library')
    async def joke(self, ctx):
        await ctx.send(pyjokes.get_joke())

    @commands.command(description='Helps you with all of lifes questions')
    async def guidance(self, ctx):
        await ctx.send(eight_answer())

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

    @commands.command(description='Displays a random fact!')
    async def facts(self, ctx):
        await ctx.send(facts())


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
        """method for cleaning chat, only administrator can use this"""

        await ctx.message.channel.purge(limit=limit)
        await ctx.channel.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

    @clean.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.channel.send("You cant do that!")

    @commands.command()
    async def slap(self, ctx):
        """Slaps the specified user"""
        try:
            user = ctx.message.mentions[0]

            await ctx.send(f'{user.mention} HOWS IT FEEL GETTING SLAPPED\n '
                           f'https://tenor.com/view/amanda-bynes-slap-gif-4079563')
        except:
            author = ctx.message.author
            await ctx.send(f'{author.mention} YOU GOTTA DO !SLAP @USERNAME \n '
                           f'https://tenor.com/view/amanda-bynes-slap-gif-4079563')

    @commands.command()
    async def covid(self, ctx):
        await ctx.send(covid_api())

    @commands.command()
    async def week(self, ctx):
        await ctx.send(week_api())


bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"),
                   description='Your friendly neighbourhood Niklas')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')
    activity = discord.Game(name=f"!help, version {VERSION}")
    await bot.change_presence(status=discord.Status.online, activity=activity)


t1 = threading.Thread(target=delete_DL)
t1.start()

# if a new class for commands is created, it needs to be added here so it can be recognised
bot.add_cog(dnd(bot))
bot.add_cog(misc(bot))
bot.add_cog(Funny(bot))
bot.add_cog(Reddit(bot))
bot.add_cog(Music(bot))
bot.run(TOKEN)
