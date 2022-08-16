import pickle
from chat_ids import chat_id
from aiogram import types, Dispatcher
import bot_defs as bd
from create_bot import bot


# @dp.message_handler(commands=['check_id'])
async def check_id(message: types.Message):
    await bot.send_message(message.from_user.id, f"Вот данные о Вас и Вашем чате\nВаш ID: {message.from_user.id}, ID чата: {message.chat.id}")
    await bot.delete_message(message.chat.id, message.message_id)


async def hello_command(message: types.Message):
    await message.answer(f"Чтобы начать взаимодействие с ботом - напиши ему в личные сообщения.\n"
                         f"<a href='https://t.me/SB_alertsBot'>*перейти в диалог*</a>",
                         parse_mode="HTML")


# @dp.message_handler(commands=['take'])
async def stop_push_dejurniy(message: types.Message):
    g = message.get_args()
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    with open(pikserver, 'rb') as f:
        servers_status = pickle.load(f)
    for i in servers_status:
        if i.alert_number == int(g):
            i.who_took = message.from_user.username
    with open(pikserver, 'wb') as f:
        pickle.dump(servers_status, f)
    await bot.send_message(chat_id, str(message.from_user.username) + ' взял в работу сервер ' +
                           str(message.get_args()))


# @dp.message_handler(commands=['dea'])
async def dea(message: types.Message):
    global server_times_name
    g = message.get_args()
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    with open(pikserver, 'rb') as f:
        servers_status = pickle.load(f)
    for i in servers_status:
        if i.name == g:
            i.active = 0
            server_times_name = i.name
    with open(pikserver, 'wb') as f:
        pickle.dump(servers_status, f)
    await message.answer(str(message.from_user.username) + ' ДЕАКТИВИРОВАЛ алерты сервера  ' + str(server_times_name))


# @dp.message_handler(commands=['act'])
async def act(message: types.Message):
    global server_times_name
    g = message.get_args()
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    with open(pikserver, 'rb') as f:
        servers_status = pickle.load(f)
    for i in servers_status:
        if i.name == g:
            i.active = 1
            server_times_name = i.name
    with open(pikserver, 'wb') as f:
        pickle.dump(servers_status, f)
    await message.answer(str(message.from_user.username) + ' АКТИВИРОВАЛ алерты сервера  ' + str(server_times_name))


# @dp.message_handler(commands=['inwork'])
async def check_servers_inwork(message: types.Message):
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    servers_inwork_list = []
    with open(pikserver, 'rb') as f:
        servers_inwork = pickle.load(f)
        for i in servers_inwork:
            if i.who_took != '':
                servers_inwork_list.append(i)
    if servers_inwork_list:
        await message.answer('Список серверов, над которыми ведутся работы \n\n' + bd.list_server(servers_inwork_list))
    else:
        await message.answer('В данный момент никто не занимается ни одним сервером')


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(hello_command, commands=['hello'])
    dp.register_message_handler(check_id, commands=['check_id'])
    dp.register_message_handler(stop_push_dejurniy, commands=['take'])
    dp.register_message_handler(dea, commands=['dea'])
    dp.register_message_handler(act, commands=['act'])
