import configparser
import time
import platform

import nextcord
from nextcord import Interaction, Locale
from nextcord.ext import commands

# class for colored console output and icons.
# You may remove this if you don't want colored console output or use your own.

class CCO:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CHECK = '\033[92m✓ \033[0m'
    RESET = '\033[0m'

# Load config file
config = configparser.ConfigParser()
config.read('config.ini')

token = config['CREDENTIALS']['token']
owner_id = str(config['CREDENTIALS']['owner_id'])
prefix = config['SETTINGS']['prefix']
status = config['SETTINGS']['status']
status_message = config['SETTINGS']['status_message']
status_type = config['SETTINGS']['status_type']

# check config file for errors
error_count = 0

if len(prefix) > 1:
    print(f'{CCO.FAIL}Error: Prefix must be only one character.{CCO.RESET}')
    error_count += 1

if status not in ['online', 'idle', 'dnd', 'invisible']:
    print(f'{CCO.FAIL}Error: Status must be one of online, idle, dnd, or invisible.{CCO.RESET}')
    error_count += 1

if status_type not in ['playing', 'streaming', 'listening', 'watching']:
    print(f'{CCO.FAIL}Error: Status type must be one of playing, streaming, listening, or watching.{CCO.RESET}')
    error_count += 1

if len(status_message) > 128:
    print(f'{CCO.FAIL}Error: Status message must be less than 128 characters.{CCO.RESET}')
    error_count += 1

if error_count > 0:
    print(f'{CCO.FAIL}Please change the config file (config.ini) and try again.\nExiting in 5 seconds...{CCO.RESET}')
    time.sleep(5)
    exit()

print(f'{CCO.CHECK}Config check.')


# discord setup
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents)


# Bot startup
@client.event
async def on_ready():
    # set status
    if status_type == 'playing':
        await client.change_presence(activity=nextcord.Game(name=status_message), status=status)
    elif status_type == 'streaming':
        await client.change_presence(activity=nextcord.Streaming(name=status_message, url='https://twich.tv'),
                                     status=status)
    elif status_type == 'listening':
        await client.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=status_message), status=status)
    elif status_type == 'watching':
        await client.change_presence(
            activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=status_message), status=status)
    # print startup message
    print(f'{CCO.CHECK}Authentication to Discord.')

    owner_name = await client.fetch_user(owner_id)
    print('======================================')
    print(f'Logged in as {CCO.BLUE}{client.user.name}#{client.user.discriminator} {CCO.RESET}({client.user.id})')
    print(f"Owner: {CCO.BLUE}{owner_name}{CCO.RESET} ({owner_id})")
    print(f'Currenly running nextcord {CCO.BLUE}{nextcord.__version__}{CCO.RESET} on python {CCO.BLUE}{platform.python_version()}{CCO.RESET}')
    print('======================================')

try:
    client.run(token)
except(nextcord.errors.LoginFailure):
    print(f'''{CCO.FAIL}Error: Token is invalid.
Please check the token in config file (config.ini) and try again.
Exiting in 5 seconds...{CCO.RESET}''')
    time.sleep(5)
    exit()