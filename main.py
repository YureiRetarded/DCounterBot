import discord
import logging
import random
import config

cfg = config.DCounterConfig()
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    print('_________________')
    print(f'Сервер:')
    print(f'{message.guild.id}')
    print(f'{message.guild.name}')
    print(f'Автор:')
    print(f'{message.author}')
    print(message.author.id)
    print(f'Сообщение:')
    print(f'{message.content}')
    print('_________________')

    if message.author == client.user:
        return

    if message.content.startswith('$random'):
        guild = client.get_guild(message.guild.id)
        number = random.randint(1, message.guild.member_count)
        user = guild.members[number - 1]
        user_id = user.id
        # await message.channel.send(user+'победитель!')
        await message.channel.send(f"<@{user_id}> is winner")


client.run(cfg.token, log_handler=handler)
