import discord 
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import time
import random
import os
from discord.ext import commands, tasks
from itertools import cycle
import operator

bot = commands.Bot(command_prefix=';')
TOKEN = os.environ['TOKEN']

bot.run(TOKEN)
