import discord
import os
import asyncio

import activity

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello Valbot'):
        await message.channel.send('Arf!')

    if message.content.startswith('$activity') and message.author.guild_permissions.administrator:
        asyncio.create_task(activity.command_activity(message, client))


client.run(os.getenv('TOKEN'))