import discord
import datetime

baselimit = 250
genlimit = 10000
## reads through the past 6000 messages in general chat, and 250 messages in each other chat and compiles the time stamps of the last message from each user, before dm-ing a txt file with: the dae of the oldest surveyed message, and a table of each username and the days since the last sent message
async def command_activity(message, client):
    guild = client.get_guild(message.guild.id)

    print(guild.name + " " + str(guild.member_count))
    ##creates table of each user with an empty date
    table = [[0, datetime.datetime(1, 1, 1).date()] for y in range(guild.member_count)]
    i = 0
    oldest_message = datetime.datetime(9999, 12, 31).date()

    for member in guild.members:
        print(str(i) + " " + member.name)
        table[i][0] = member.name
        i = i + 1
    ##gets the most recent messages from each channel finding the most recent message from each user
    for channel in guild.text_channels:
        limit = baselimit
        print(channel.name)
        if channel.name == "general" or channel.id == 1236856577596719138:
            limit = genlimit
        if channel.permissions_for(guild.me).read_messages:
            async for post in channel.history(limit=limit):
                for i in range(guild.member_count):
                    if table[i][0] == post.author.name and table[i][1] < post.created_at.date():
                        table[i][1] = post.created_at.date()
                    if limit == genlimit and post.created_at.date() < oldest_message:
                        oldest_message = post.created_at.date()
    ##when loop ends create txt file, and write the table to it, before dming it to whomever called the bot
    else:
        with (open("table.txt", "w") as file):
            i = 0
            file.write(f'Days since oldest message surveyed in general: {(oldest_message - table[i][1]).days}\n')
            file.write("Username : days since last message\n")
            for row in table:
                if table[i][1] < oldest_message:
                    file.write(f'{table[i][0]} : prior to last surveyed message\n')
                else:
                    file.write(f'{table[i][0]} : {(datetime.datetime.today().date() - table[i][1]).days}\n')
                i = i + 1
        dm = await client.create_dm(message.author)
        await dm.send(file=discord.File('table.txt'), content='arf arf!')