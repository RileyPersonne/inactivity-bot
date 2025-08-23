import discord
import datetime
import asyncio
import os

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
        guild = client.guilds[0]
        table = [[0 for x in range(2)] for y in range(guild.member_count)]
        i = 0

        for member in guild.members:
            table[0][i] = member.name
            table[1][i] = datetime.datetime(1,1,1).date()
            i = i + 1

        for channel in guild.text_channels:
            async for message in channel.history(limit=500):
                for i in range(guild.member_count):
                    if table[0][i] == message.author.name:
                        if table[1][i] < message.created_at.date():
                            table[1][i] = message.created_at.date()

        with (open("table.txt", "w") as file):
            i = 0
            for row in table:
                file.write(f'{table[0][i]} : {(datetime.datetime.today().date()-table[1][i]).days}\n')
                i = i + 1

        dm = await client.create_dm(message.author)
        await dm.send(file=discord.File('table.txt'), content='arf arf!')

client.run(os.getenv('TOKEN'))
