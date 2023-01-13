import discord
import logging
import random
import config
import db_adapater

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
    # print('_________________')
    # print(f'Сервер:')
    # print(f'{message.guild.id}')
    # print(f'{message.guild.name}')
    # print(f'Автор:')
    # print(f'{message.author}')
    # print(message.author.id)
    # print(f'Сообщение:')
    # print(f'{message.content}')
    # print('_________________')

    if message.author == client.user:
        return

    if message.content.startswith('$random'):
        guild = client.get_guild(message.guild.id)
        members = guild.members
        db_adapater.update_members_guild(guild.id, members)
        number = random.randint(1, message.guild.member_count)
        user = guild.members[number - 1]
        user_id = user.id
        id_server = db_adapater.get_server(guild.id)[0][0]
        nom = db_adapater.get_nomination(id_server)[0]
        if id_server == None:
            await message.channel.send(f"Зарегистрируйте сервер командой $regServer")
        elif nom == None:
            await message.channel.send(f"Добавьте номинацию командой $addNom 'Название номинации'")
        else:
            id_user = db_adapater.get_user(guild.id, user_id)[0][0]
            db_adapater.add_user_to_nominate(nom[0], id_user)
            await message.channel.send(f"<@{user_id}> {nom[1]}")

    if message.content.startswith('$list'):
        guild = client.get_guild(message.guild.id)
        id_server = db_adapater.get_server(guild.id)[0][0]
        list = db_adapater.get_nomination_users_by_server(id_server)
        if list != None:
            mes = f'Список наших победителей на звание "{list[0][2]}"\n Имя - Количество\n\n'
            for row in list:
                mes_row = f'<@{row[1]}> - {row[0]}\n'
                mes = mes + mes_row
            await message.channel.send(mes)
        else:
            await message.channel.send("Вы ещё не разу не разыгрывали звание среди участников!")

    if message.content.startswith('$regServer'):
        server = db_adapater.get_server(message.guild.id)
        if server != None:
            await message.channel.send("Сервер уже зарегистрирован!")
        else:
            db_adapater.create_server(message.guild.id)
            guild = client.get_guild(message.guild.id)
            members = guild.members
            db_adapater.update_members_guild(guild.id, members)
            await message.channel.send("Сервак зарегистрирован!")

    # if message.content.startswith('$regPeople'):
    #     guild = client.get_guild(message.guild.id)
    #     members = guild.members
    #     db_adapater.update_members_guild(guild.id, members)
    #     await message.channel.send("Список обновлён")

    if message.content.startswith('$addNom'):
        text = message.content.split(' ')
        if len(text) > 1 and text[1] != ' ':
            result = db_adapater.create_nomination(db_adapater.get_server(message.guild.id)[0][0], text[1])
            if result != None:
                await message.channel.send(result[1])
            else:
                await message.channel.send("Номинация добавлена")
        else:
            await message.channel.send("Ошибка при добавлении номинации")

    if message.content.startswith('$help'):
        text='Список команд бота:\n$regServer - Регистрация сервера\n$addNom *название* - Название вашей номинации\n$random - Проведения розыгрыша\n$list - список участников и их количество побед\nВерсия бота: 0.2.0'
        await message.channel.send(text)

client.run(cfg.token, log_handler=handler)
