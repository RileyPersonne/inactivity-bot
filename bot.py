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
        oldest_message = datetime.datetime(9999,9999,9999).date()

        for member in guild.members:
            table[0][i] = member.name
            table[1][i] = datetime.datetime(1,1,1).date()
            i = i + 1

        for channel in guild.text_channels:
            limit=250
            if channel.id == 1236856577596719138:
                limit=6000
            async for message in channel.history(limit=limit):
                for i in range(guild.member_count):
                    if table[0][i] == message.author.name and table[1][i] < message.created_at.date():
                            table[1][i] = message.created_at.date()
                if limit==6000 and message.create_at.date() < oldest_message:
                    oldest_message = message.created_at.date()

        with (open("table.txt", "w") as file):
            i = 0
            file.write(f'oldest message surveyed in general: {oldest_message}\n')
            for row in table:
                if table[1][i] == oldest_date:
                    file.write(f'{table[0][i]} : prior to last surveyed message\n')
                else:
                    file.write(f'{table[0][i]} : {(datetime.datetime.today().date()-table[1][i]).days}\n')
                i = i + 1

        dm = await client.create_dm(message.author)
        await dm.send(file=discord.File('table.txt'), content='arf arf!')

client.run(os.getenv('TOKEN'))
