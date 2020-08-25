import json
import sys
import os
import copy
import traceback
import discord
import subprocess
from subprocess import Popen
from discord.ext import commands
from discord import utils

MASTER_CONFIG = dict()
SERVER_CONFIGS = dict()
MASTER_LOADED = False
BOT = None

CONFIG_TEMPLATE = {
    "NONRANKED-NA": 0,
    "RANKED-NA": 0,
    "NONRANKED-EU": 0,
    "RANKED-EU": 0, 
    "NONRANKED-OTHER": 0,
    "RANKED-OTHER": 0,
    "PULLROOMROLE": 0,
    "PULLROOM": 0,
    "PULLROOMLOG": 0,
    "MODROLE": 0,
    "LOGGING": 0,
    "EMERGENCY": 0,
    "RANKED": [],
    "NONRANKED": [],
    "UNSUPPORTED": [],
    "CENSOR": [],
    "NONEMERGENCY": []
}

def initialize(bot):
    global BOT
    BOT = bot
    
async def onReady(bot:commands.Bot):
    print(f"Loading configurations for {len(bot.guilds)} guilds")
    for guild in bot.guilds:
        if guild.id == 679875946597056683:
            VALORANT = "VALORANT"
            print(f"Loading info for {VALORANT} ({guild.id})")
            loadConfig(guild)
        else:
            print(f"Loading info for {guild.name} ({guild.id})")
            loadConfig(guild)


def loadGlobalConfig():
    global MASTER_CONFIG
    try:
        with open('config/master.json', 'r') as jsonfile:
            MASTER_CONFIG = json.load(jsonfile)
    except FileNotFoundError:
        print("Unable to load config, running with defaults.")
    except Exception as e:
        print("Failed to parse configuration.")
        print(e)
        raise e


def loadConfig(guild:discord.Guild):
    global SERVER_CONFIGS
    try:
        with open(f'config/{guild.id}.json', 'r') as jsonfile:
            config = json.load(jsonfile)
            for key in CONFIG_TEMPLATE:
                if key not in config:
                    config[key] = CONFIG_TEMPLATE[key]
            SERVER_CONFIGS[guild.id] = config
    except FileNotFoundError:
        print(f"No config available for {guild.name} ({guild.id}), creating blank one.")
        SERVER_CONFIGS[guild.id] = copy.deepcopy(CONFIG_TEMPLATE)
        saveConfig(guild.id)

def getConfigVar(id, key):
    if id not in SERVER_CONFIGS.keys():
        loadConfig(id)
    return SERVER_CONFIGS[id][key]

def getConfigVarChannel(id, key, bot:commands.Bot):
    return bot.get_channel(getConfigVar(id, key))

def setConfigVar(id, key, value):
    SERVER_CONFIGS[id][key] = value
    saveConfig(id)

def saveConfig(id):
    global SERVER_CONFIGS
    with open(f'config/{id}.json', 'w') as jsonfile:
        jsonfile.write((json.dumps(SERVER_CONFIGS[id], indent=4, skipkeys=True, sort_keys=True)))

def getMasterConfigVar(key, default=None) :
    global MASTER_CONFIG
    if not key in MASTER_CONFIG.keys():
        MASTER_CONFIG[key] = default
        saveMasterConfig()
    return MASTER_CONFIG[key]


def saveMasterConfig():
    global MASTER_CONFIG
    with open('config/master.json', 'w') as jsonfile:
        jsonfile.write((json.dumps(MASTER_CONFIG, indent=4, skipkeys=True, sort_keys=True)))

### Other things unrelated to Configuration

def paginate(input, max_lines=30, max_chars=1850, prefix="", suffix=""):
    max_chars -= len(prefix.format(page=100, pages=100)) + len(suffix.format(page=100, pages=100))
    lines = str(input).splitlines(keepends=True)
    pages = list()
    page = ""
    count = 0
    for line in lines:
        if len(page) + len(line) > max_chars or count == max_lines:
            if page == "":
                # single 2k line, split smaller
                words = line.split(" ")
                for word in words:
                    if len(page) + len(word) > max_chars:
                        pages.append(page)
                        page = f"{word} "
                    else:
                        page += f"{word} "
            else:
                pages.append(page)
                page = line
                count = 1
        else:
            page += line
        count += 1
    pages.append(page)
    page_count = 1
    total_pages = len(pages)
    real_pages = list()
    for page in pages:
        real_pages.append(f"{prefix.format(page=page_count, pages=total_pages)}{page}{suffix.format(page=page_count, pages=total_pages)}")
    return real_pages
