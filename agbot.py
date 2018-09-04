import discord
import asyncio
import threading
import config
from agmapkey import AGMapKey

client = discord.Client()

@client.event
async def on_ready():
    #needs to calculate start of hour and then call a reset method
    await client.send_message(discord.Object(id=config.channel), 'Ready')

@client.event
async def on_message(message):
    if message.content.startswith('!showmaps'):
        await show_maps(message)
    elif message.content.startswith('!addmap'):
        await add_map(message)
    elif message.content.startswith('!removemap'):
        await remove_map(message)
    elif message.content.startswith('!enableverbose'):
        config.verbose = True
        await client.send_message(message.channel, 'Verbose mode enabled')
    elif message.content.startswith('!disableverbose'):
        config.verbose = False
        await client.send_message(message.channel, 'Verbose mode disabled')

async def show_maps(message):
    for key, value in config.maps.items():
        if config.verbose:
            await client.send_message(message.channel, str(key) + "\n " +  value)

async def add_map(message):
    name =  message.author.display_name
    firstspacepos = message.content.find(' ')
    content = ''
    if firstspacepos != -1:
        content = message.content[firstspacepos + 1:]
    attachments = message.attachments
    for attachment in attachments:
        try:
            config.maps[AGMapKey(name, content)] = attachment['url']
        except:
            print('Attachment has no url')
            print(attachment)
    if config.verbose:
        await client.send_message(message.channel, 'Added ' + content + ' from ' + name)

async def remove_map(message):
    name =  message.author.display_name
    content = ''
    firstspacepos = message.content.find(' ')
    if firstspacepos != -1:
        content = message.content[firstspacepos + 1:]
    config.maps.pop(AGMapKey(name, content), None)
    if config.verbose:
        await client.send_message(message.channel, 'Removed ' + content + ' from ' + name)

async def reset_maps():
    config.maps = {}
    #call firebase and reset

def initBot():
    #need to calculate start of hour and call reset method
    client.run(config.token)