import discord
import datetime
import os
import asyncio

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


async def command_activity(message):
    guild = client.get_guild(message.guild.id)

    print(guild.name + " " + str(guild.member_count))

    table = [[0, datetime.datetime(1, 1, 1).date()] for y in range(guild.member_count)]
    i = 0
    oldest_message = datetime.datetime(9999, 12, 31).date()

    for member in guild.members:
        print(str(i) + " " + member.name)
        table[i][0] = member.name
        i = i + 1

    for channel in guild.text_channels:
        limit = 250
        if channel.name == "general":
            limit = 6000
        async for post in channel.history(limit=limit):
            for i in range(guild.member_count):
                if table[i][0] == post.author.name and table[i][1] < post.created_at.date():
                    table[i][1] = post.created_at.date()
                if limit == 6000 and post.created_at.date() < oldest_message:
                    oldest_message = post.created_at.date()
    else:
        with (open("table.txt", "w") as file):
            i = 0
            file.write(f'oldest message surveyed in general: {oldest_message}\n')
            for row in table:
                if table[i][1] == oldest_message:
                    file.write(f'{table[i][0]} : prior to last surveyed message\n')
                else:
                    file.write(f'{table[i][0]} : {(datetime.datetime.today().date() - table[i][1]).days}\n')
                    i = i + 1
        dm = await client.create_dm(message.author)
        await dm.send(file=discord.File('table.txt'), content='arf arf!')
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
        asyncio.create_task(command_activity(message))


client.run(os.getenv('TOKEN'))