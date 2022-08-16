import pickle
import random
import re

import bot_settings
from sql import execute_query, connection, execute_read_query
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types.web_app_info import WebAppInfo
import bot_defs
from chat_ids import chat_id
from create_bot import bot
from dejurnie import dejurnie


def check_adm():
    """Проверка на администратора"""
    pikperson = "/projects/sb_bot/data/pikperson.dat"
    with open(pikperson, 'rb') as f:
        adm_list = pickle.load(f)
    admins = ()
    for adm in adm_list:
        admins = admins + (adm.telegram_id,)
    return admins


async def handle_unwanted_users(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id, "Это меню только для SD\n"
                                             "Чтобы попасть в отряд администраторов - пиши /reg ", show_alert=True)

main_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('\U0001F6B6 Меню пользователя \U0001F6B6',
                                                 callback_data='btnUsermenu', state=None)
                        ],
                        [
                            InlineKeyboardButton('\U0001F47E Меню дежурного \U0001F47E',
                                                 callback_data='btnDejmenu')
                        ],
                        [
                            InlineKeyboardButton('\U0001F3B2 Лучшее в мире число \U0001F3B2',
                                                 callback_data='btnRandom'),
                        ],
                        [
                            InlineKeyboardButton('Выход', callback_data='btnExit')
                        ]
                    ]
    )
second_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Список дежурных', callback_data='dej_spisok'),
                            InlineKeyboardButton('Список персонала', callback_data='sotr_spisok')
                        ],
                        [
                            InlineKeyboardButton('Снять алерт после падения электричества',
                                                 callback_data='dea_alert_220')
                        ],
                        [
                            InlineKeyboardButton('Управление серверами', callback_data='server_menu')
                        ],
                        [
                            InlineKeyboardButton('Посмотреть заявки', callback_data='request_menu')
                        ],
                        [
                            InlineKeyboardButton('Настройки бота', callback_data='bot_settings')
                        ],
                        [
                            InlineKeyboardButton('Зарегистрироваться в боте ( для отладки )',
                                                 callback_data='register_in_bot')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в главное меню \U0001F519', callback_data='level_0')
                        ]
                    ]
)

bot_settings_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Изменить периодичность пинга серверов',
                                                 callback_data='change_server_time_to_ping')
                        ],
                        [
                            InlineKeyboardButton('Изменить периодичность алертов на сотрудника',
                                                 callback_data='change_alert_time')
                        ],
                        [
                            InlineKeyboardButton('Изменить время, для перехода на сл.сотрудника',
                                                 callback_data='change_next_time')
                        ],
                        [
                            InlineKeyboardButton('Включить/выключить алерты бота',
                                                 callback_data='switch_on_off_bot_alerts')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню дежурного \U0001F519', callback_data='btnDejmenu')
                        ]
                    ]
)


bot_settings_menu_update_timer = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('90 секунд', callback_data='update_timer 90'),
                            InlineKeyboardButton('180 секунд', callback_data='update_timer 180')
                        ],
                        [
                            InlineKeyboardButton('240 секунд', callback_data='update_timer 240'),
                            InlineKeyboardButton('300 секунд', callback_data='update_timer 300')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню настроек \U0001F519', callback_data='bot_settings')
                        ]
                    ]
)
bot_settings_menu_priory_timer = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('90 секунд', callback_data='priory_timer 90'),
                            InlineKeyboardButton('180 секунд', callback_data='priory_timer 180')
                        ],
                        [
                            InlineKeyboardButton('240 секунд', callback_data='priory_timer 240'),
                            InlineKeyboardButton('300 секунд', callback_data='priory_timer 300')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню настроек \U0001F519', callback_data='bot_settings')
                        ]
                    ]
)
bot_settings_menu_alert_timer = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('90 секунд', callback_data='alert_timer 90'),
                            InlineKeyboardButton('180 секунд', callback_data='alert_timer 180')
                        ],
                        [
                            InlineKeyboardButton('240 секунд', callback_data='alert_timer 240'),
                            InlineKeyboardButton('300 секунд', callback_data='alert_timer 300')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню настроек \U0001F519', callback_data='bot_settings')
                        ]
                    ]
)
bot_settings_menu_active_yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Включить', callback_data='alerts_is_active True'),
                            InlineKeyboardButton('Выключить', callback_data='alerts_is_active False')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню настроек \U0001F519', callback_data='bot_settings')
                        ]
                    ]



)
server_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Список серверов', callback_data='list_server_menu'),
                            InlineKeyboardButton('Сервера "в работе"', callback_data='inwork_spisok')
                        ],
                        [
                            InlineKeyboardButton('Добавить новый сервер', callback_data='add_server'),
                            InlineKeyboardButton('Удалить сервер', callback_data='remove_server'),
                        ],
                        [
                            InlineKeyboardButton('Посмотреть камеру серверной',
                                                 web_app=WebAppInfo(
                                                     url="https://cb7a-178-170-230-253.eu.ngrok.io/servernaya"))
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню дежурного \U0001F519', callback_data='btnDejmenu')
                        ]
                    ]
)

list_server_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Список Major серверов', callback_data='major'),
                            InlineKeyboardButton('Список Secondary серверов', callback_data='secondary'),
                            InlineKeyboardButton('Список Common серверов', callback_data='common')
                        ],
                        [
                            InlineKeyboardButton('Список неисправных серверов', callback_data='down')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в  главное меню \U0001F519', callback_data='server_menu')
                        ]
                    ]
)

third_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Отправить заявку в СД \U0001F4AC',
                                                 callback_data='make_request')
                        ],
                        [
                            InlineKeyboardButton('Посмотреть свои заявки \U00002753', callback_data='my_requests')
                        ],
                        [
                            InlineKeyboardButton('Посмотреть, кто сегодня дежурный \U0001F4C5',
                                                 callback_data='who_is_dejurniy?')
                        ],
                        [
                            InlineKeyboardButton('Сотрудники сервис деска \U0000260E',
                                                 callback_data='list_all_sd')
                        ],
                        [
                            InlineKeyboardButton('Обстановка в столовой \U0001F354',
                                                 web_app=WebAppInfo(
                                                     url="https://cb7a-178-170-230-253.eu.ngrok.io/stolovaya"))
                        ],
                        [
                            InlineKeyboardButton('Места на парковке \U0001F697',
                                                 web_app=WebAppInfo(
                                                     url="https://cb7a-178-170-230-253.eu.ngrok.io/parkovka"))
                        ],
                        [
                            InlineKeyboardButton(text='Информационный собрат Балансик',
                                                 url="https://t.me/SB_guide_bot")
                        ],
                        [
                            InlineKeyboardButton('Вернуться в главное меню \U0001F519',
                                                 callback_data='level_0')
                        ]
                    ]
)


async def level_0(call: types.CallbackQuery):
    await bot.edit_message_text('Главное меню.', call.from_user.id, call.message.message_id, reply_markup=main_menu)


async def level_0_0(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.delete_message(message.from_user.id, message.message_id)
    await bot.send_message(message.from_user.id, 'Добро пожаловать, Вы в главном меню.\n', reply_markup=main_menu)


"""Регистрация сотрудника SD"""
sd_i_ladno = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Ну и ладно..', callback_data='i_ladno')
                        ]
    ]
)

sd_priory_kb = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Начальник отдела', callback_data='3')
                        ],
                        [
                            InlineKeyboardButton('Системный администратор', callback_data='1')
                        ],
                        [
                            InlineKeyboardButton('Младший системный администратор', callback_data='2')
                        ]
                    ]
)

sd_priory_accept = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Все верно', callback_data='sd_yes')
                        ],
                        [
                            InlineKeyboardButton('Не верно, отменить', callback_data='sd_no')
                        ]
                    ]
)


class Order_sd(StatesGroup):
    waiting_for_key = State()
    waiting_for_fio = State()
    waiting_for_priory = State()
    waiting_for_phone = State()
    waiting_for_accept = State()


async def sd_key(message: types.Message, state: FSMContext):
    await bot.delete_message(message.from_user.id, message.message_id)
    msg = await message.answer('Введи ключ авторизации администратора')

    await Order_sd.waiting_for_key.set()
    await state.update_data(to_del=msg.message_id)


async def sd_fio(message: types.Message, state: FSMContext):
    from credentials import adm_key
    request_data = await state.get_data()
    await bot.delete_message(message.from_user.id, request_data['to_del'])
    await bot.delete_message(message.from_user.id, message.message_id)
    if message.text != f'{adm_key}':
        await message.answer('Не думаю, что ты сотрудник SD..', reply_markup=sd_i_ladno)
        await state.finish()
    else:
        msg = await message.answer('Введи фио в формате\n'
                                   'ИМЯ ФАМИЛИЯ \n'
                                   'Например : Басин Роман')
        await Order_sd.next()
        await state.update_data(to_del=msg.message_id)


async def sd_priory(message: types.Message, state: FSMContext):
    request_data = await state.get_data()

    if not re.match("([а-яА-Яa-zA-Z]{1,}\s[а-яА-Яa-zA-Z]{1,})", message.text):
        try:
            await bot.edit_message_text('Неверно введены данные\n'
                                        'Используй формат : ИМЯ ФАМИЛИЯ',
                                        message.chat.id, request_data['to_del'])
            await bot.delete_message(message.from_user.id, message.message_id)
        except:
            await bot.delete_message(message.from_user.id, message.message_id)
    else:
        await bot.delete_message(message.from_user.id, message.message_id)

        await bot.delete_message(message.from_user.id, request_data['to_del'])
        msg = await message.answer('Какая у тебя должность?', reply_markup=sd_priory_kb)
        await state.update_data(fio=message.text)
        await state.update_data(to_del=msg.message_id)
        await Order_sd.next()


async def sd_phone(call: types.CallbackQuery, state: FSMContext):
    request_data = await state.get_data()
    await bot.delete_message(call.from_user.id, request_data['to_del'])
    await state.update_data(priory=str(call.data))
    msg = await bot.send_message(call.from_user.id, 'Какие у тебя номера телефона?\n'
                                                    'Короткий номер и мобильный номер\n'
                                                    'Например: 581 89217625037')
    await state.update_data(to_del=msg.message_id)
    await Order_sd.next()


async def sd_complete(message: types.Message, state: FSMContext):
    request_data = await state.get_data()
    if not re.match("([0-9]{1,}\s[0-9]{1,})", message.text):
        try:
            await bot.edit_message_text('Неверно введены данные\n'
                                        'Используй формат: 567 89217625037',
                                        message.chat.id, request_data['to_del'])
            await bot.delete_message(message.from_user.id, message.message_id)
        except:

            await bot.delete_message(message.from_user.id, message.message_id)
    else:
        await bot.delete_message(message.from_user.id, message.message_id)

        await bot.delete_message(message.from_user.id, request_data['to_del'])
        await state.update_data(numbers=message.text)
        await state.update_data(telegram_id=int(message.from_user.id))
        await state.update_data(telegram_name=message.from_user.username)
        request_data = await state.get_data()
        msg = await bot.send_message(message.from_user.id, f"Подтверди данные:\n"
                                                           f"ФИО - {request_data['fio']}\n"
                                                           f"Должность - {request_data['priory']}\n"
                                                           f"Телефонные номера - {request_data['numbers']}\n"
                                                           f"Данные Telegram:\n"
                                                           f"id - {request_data['telegram_id']}\n"
                                                           f"telegram_username - {request_data['telegram_name']}",
                                     reply_markup=sd_priory_accept)
        await state.update_data(to_del=msg.message_id)
        await Order_sd.next()


async def sd_accept(call: types.CallbackQuery, state: FSMContext):
    request_data = await state.get_data()
    if call.data == 'sd_yes':
        await bot.answer_callback_query(call.id, 'Регистрация завершена.\n'
                                                 'Теперь тебе доступно меню дежурного.', show_alert=True)
        add_sd_person = """
                            INSERT INTO 
                                admins (name, telegram_name, telegram_id, short_number, long_number, priory,
                                 is_dejurniy)
                            VALUES
                                (?,?,?,?,?,?,?)
                            ON CONFLICT(name) DO NOTHING
                        """
        execute_query(connection, add_sd_person, [(request_data['fio'], request_data['telegram_name'],
                                                   request_data['telegram_id'], request_data['numbers'].split()[0],
                                                  request_data['numbers'].split()[1], request_data['priory'], 0)])
        await bot_defs.update_pikperson_from_bd()
    elif call.data == 'sd_no':
        await bot.answer_callback_query(call.id, 'Чтобы повторить попытку - напиши /reg', show_alert=True)
    await state.finish()
    await bot.delete_message(call.from_user.id, request_data['to_del'])


async def randoms(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Забавно, но это число : {0}'.format(random.randint(0, 100)),
                           reply_markup=main_menu)


async def second_men(call: types.CallbackQuery):
    await bot.edit_message_text('Меню дежурного.', call.from_user.id, call.message.message_id,
                                reply_markup=second_menu)


async def third_men(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text('Меню пользователя.', call.from_user.id, call.message.message_id,
                                reply_markup=third_menu)


async def dej_spisok(call: types.CallbackQuery):
    i = bot_defs.list_dej_calendar(dejurnie())
    await bot.edit_message_text(i, call.from_user.id, call.message.message_id, reply_markup=second_menu)


async def server_men(call: types.CallbackQuery):
    await bot.edit_message_text('Меню управления серверами.', call.from_user.id, call.message.message_id,
                                reply_markup=server_menu)


async def bot_settings_men(call: types.CallbackQuery):
    settings_list = bot_settings.read_settings_all()
    await bot.edit_message_text(f"Меню настроек бота\n\n"
                                f"Пинги отрабатывают каждые {settings_list['update_timer']} секунд\n"
                                f"Алерты отправляются каждые {settings_list['alert_timer']} секунд\n"
                                f"Переход алертов на другого сотрудника в течении"
                                f" {settings_list['priory_timer']} секунд\n"
                                f"Оповещения работают: {settings_list['alerts_is_active']}", call.from_user.id,
                                call.message.message_id, reply_markup=bot_settings_menu)


async def list_all_sd(call: types.CallbackQuery):
    pikperson = "/projects/sb_bot/data/pikperson.dat"
    with open(pikperson, 'rb') as f:
        spisok_adminov = pickle.load(f)
    if spisok_adminov:
        await bot.edit_message_text(bot_defs.list_person(spisok_adminov), call.from_user.id,
                                    call.message.message_id, reply_markup=third_menu,
                                    parse_mode="HTML", disable_web_page_preview=True)
    else:
        await bot.edit_message_text('В данный момент  в штате SD нет ни одного сотрудника', call.from_user.id,
                                    call.message.message_id, reply_markup=third_menu)


async def list_my_requests(call: types.CallbackQuery):
    from sql import execute_read_query_with_par
    person_id = call.from_user.id
    select_from_comments = """SELECT * FROM comments WHERE telegram_id = (?)"""
    selected_from_comments = execute_read_query_with_par(connection, select_from_comments, (person_id,))
    if selected_from_comments:
        await bot.edit_message_text(f'Ваши обращения:\n {bot_defs.list_request(selected_from_comments, "user")}',
                                    call.from_user.id, call.message.message_id, reply_markup=third_menu)
    else:
        await bot.edit_message_text(f'У вас нету обращений в службу Сервис-Деск',
                                    call.from_user.id, call.message.message_id, reply_markup=third_menu)


async def list_today_dejurniy(call: types.CallbackQuery):
    import datetime
    today = datetime.date.today()
    found = False
    pikperson = "/projects/sb_bot/data/pikperson.dat"
    with open(pikperson, 'rb') as f:
        spisok_adminov = pickle.load(f)
    if spisok_adminov:
        for admin in spisok_adminov:
            if admin.is_dejurniy == 1:
                await bot.edit_message_text(f"Сегодня {today}\n"
                                            f"Дежурный в этот день {admin.name}\n"
                                            f"Короткий номер сотрудника {admin.short_number}\n"
                                            f"Мобильный номер {admin.long_number}\n"
                                            f"Городской телефон  372-50-08",
                                            call.from_user.id, call.message.message_id, reply_markup=third_menu)
                found = True
                break
        if not found:
            await bot.edit_message_text('Увы, сегодня никто не дежурит..\n'
                                        'Но тебе никто не мешает обратиться к любому сотруднику SD\n',
                                        call.from_user.id, call.message.message_id, reply_markup=third_menu)
    else:
        await bot.edit_message_text('Увы, сегодня никто не дежурит..\n'
                                    'Но тебе никто не мешает обратиться к любому сотруднику SD\n',
                                    call.from_user.id, call.message.message_id, reply_markup=third_menu)


async def register_in_bot(call: types.CallbackQuery):
    import bot_defs
    telegram_name = call.from_user.username
    telegram_id = call.from_user.id
    add_telegram_id = """
                        UPDATE
                            admins
                        SET
                            telegram_id = ?
                        WHERE
                            telegram_name = ?                                                          
                      """
    execute_query(connection, add_telegram_id, [(telegram_id, telegram_name)])
    await bot_defs.update_pikperson_from_bd()
    await bot.edit_message_text(f'передал твой id{telegram_id} боту.\nТеперь ты сможешь получать '
                                f'увдомления в личных сообщениях',
                                call.from_user.id, call.message.message_id, reply_markup=second_menu)


async def sotr_spisok(call: types.CallbackQuery):
    pikperson = "/projects/sb_bot/data/pikperson.dat"
    with open(pikperson, 'rb') as f:
        spisok_adminov = pickle.load(f)
    await bot.edit_message_text(bot_defs.list_person(spisok_adminov), call.from_user.id,
                                call.message.message_id, reply_markup=second_menu)


async def serv_spisok(call: types.CallbackQuery):
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    with open(pikserver, 'rb') as f:
        servers_status = pickle.load(f)
    msg_to_edit = bot_defs.tab_list(servers_status)

    await bot.edit_message_text(msg_to_edit, call.from_user.id,
                                call.message.message_id, reply_markup=server_menu)


async def list_servers_with_category(call: types.CallbackQuery):
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    if str(call.data) == 'major':
        with open(pikserver, 'rb') as f:
            servers = pickle.load(f)
        to_list = bot_defs.tab_list_major(servers, str(call.data))
        if to_list:
            await bot.edit_message_text(f'Список Major серверов\n\n{to_list}',
                                        call.from_user.id, call.message.message_id, reply_markup=list_server_menu)
        else:
            await bot.edit_message_text(
                f'Список важных серверов\n\nВ данный момент я не мониторю сервера со статусом major',
                call.from_user.id, call.message.message_id, reply_markup=list_server_menu)

    elif str(call.data) == 'secondary':
        with open(pikserver, 'rb') as f:
            servers = pickle.load(f)
        to_list = bot_defs.tab_list_major(servers, str(call.data))
        if to_list:
            await bot.edit_message_text(f'Список Secondary серверов\n\n{to_list}',
                                        call.from_user.id, call.message.message_id, reply_markup=list_server_menu)
        else:
            await bot.edit_message_text(
                f'Список важных серверов\n\nВ данный момент я не мониторю сервера со статусом secondary',
                call.from_user.id, call.message.message_id, reply_markup=list_server_menu)

    elif str(call.data) == 'common':
        with open(pikserver, 'rb') as f:
            servers = pickle.load(f)
        to_list = bot_defs.tab_list_major(servers, str(call.data))
        if to_list:
            await bot.edit_message_text(f'Список Common серверов\n\n{to_list}',
                                        call.from_user.id, call.message.message_id, reply_markup=list_server_menu)
        else:
            await bot.edit_message_text(
                f'Список важных серверов\n\nВ данный момент я не мониторю сервера со статусом Common',
                call.from_user.id, call.message.message_id, reply_markup=list_server_menu)

    elif str(call.data) == 'down':
        with open(pikserver, 'rb') as f:
            servers = pickle.load(f)
        to_list = bot_defs.tab_list_major(servers, str(call.data))
        if to_list:
            await bot.edit_message_text(f'Список неисправных серверов\n\n{to_list}',
                                        call.from_user.id, call.message.message_id, reply_markup=list_server_menu)
        else:
            await bot.edit_message_text(
                f'Список неисправных серверов\n\nВ данный момент нет неисправных серверов',
                call.from_user.id, call.message.message_id, reply_markup=list_server_menu)


async def inwork_spisok(call: types.CallbackQuery):
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    servers_inwork_list = []
    with open(pikserver, 'rb') as f:
        servers_inwork = pickle.load(f)
        for i in servers_inwork:
            if i.who_took != '':
                servers_inwork_list.append(i)
    if servers_inwork_list:
        await bot.edit_message_text('Список серверов, над которыми ведутся работы \n\n' +
                                    bot_defs.list_server(servers_inwork_list), call.from_user.id,
                                    call.message.message_id, reply_markup=server_menu)
    else:
        await bot.edit_message_text('В данный момент никто не занимается ни одним сервером',
                                    call.from_user.id, call.message.message_id, reply_markup=server_menu)


"""Управление заявками"""

request_menu = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Свободные заявки', callback_data='free_requests')
                        ],
                        [
                            InlineKeyboardButton('Заявки в работе', callback_data='taken_requests')
                        ],
                        [
                            InlineKeyboardButton('Архив заявок', callback_data='archive_requests')
                        ],
                        [
                            InlineKeyboardButton('Вернуться в меню дежурного \U0001F519', callback_data='btnDejmenu')
                        ]

                    ]
)

to_do_with_req_free = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Взять заявку в работу', callback_data='take_request')
        ],
        [
            InlineKeyboardButton('Закрыть заявку(выполнена)', callback_data='complete_request')
        ],
        [
            InlineKeyboardButton('Удалить заявку', callback_data='delete_request')
        ],
        [
            InlineKeyboardButton('Вернуться в меню заявок', callback_data='request_menu')
        ]
    ]
)

to_do_with_req_taken = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Закрыть заявку(выполнена)', callback_data='complete_request')
        ],
        [
            InlineKeyboardButton('Удалить заявку', callback_data='delete_request')
        ],
        [
            InlineKeyboardButton('Вернуться в меню заявок', callback_data='request_menu')
        ]
    ]
)

to_do_with_req_archive = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton('Удалить заявку', callback_data='delete_request')
        ],
        [
            InlineKeyboardButton('Вернуться в меню заявок', callback_data='request_menu')
        ]
    ]
)


class Order_request_menu(StatesGroup):
    wait_for_choose = State()
    wait_for_action = State()
    wait_for_action_complete = State()


async def req_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id, reply_markup=request_menu)


async def archive_req(call: types.CallbackQuery, state: FSMContext):
    if call.data == "request_menu":
        await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id,
                                    reply_markup=request_menu)
    else:
        from sql import execute_read_query_with_par
        select_archive_req = """SELECT * FROM comments WHERE dej = (?) and completed = 'yes' """
        selected_archive_req = execute_read_query_with_par(connection, select_archive_req, (call.from_user.id,))
        button_list = []
        for i in selected_archive_req:
            button_to_add = InlineKeyboardButton(f'{i[0]}', callback_data=f'{i[0]}')
            button_list.append(button_to_add)
        free_req_buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                button_list,
                [InlineKeyboardButton('Вернуться в меню заявок', callback_data='request_menu')]
            ]
        )
        await state.update_data(var=call.data)
        await Order_request_menu.wait_for_choose.set()
        await bot.edit_message_text(f'Архив заявок:\n{bot_defs.list_request(selected_archive_req, "full")}',
                                    call.from_user.id, call.message.message_id, reply_markup=free_req_buttons)


async def free_req(call: types.CallbackQuery, state: FSMContext):
    if call.data == "request_menu":
        await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id,
                                    reply_markup=request_menu)
    else:
        select_all_requests = """SELECT * FROM comments WHERE dej IS NULL"""
        all_requests = execute_read_query(connection, select_all_requests)
        button_list = []
        for i in all_requests:
            button_to_add = InlineKeyboardButton(f'{i[0]}', callback_data=f'{i[0]}')
            button_list.append(button_to_add)

        free_req_buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                                button_list,
                                [InlineKeyboardButton('Вернуться в меню заявок', callback_data='request_menu')]
                            ]
        )
        await state.update_data(var=call.data)
        await Order_request_menu.wait_for_choose.set()
        await bot.edit_message_text('Список свободных заявок', call.from_user.id,
                                    call.message.message_id, reply_markup=free_req_buttons)


async def taken_req(call: types.CallbackQuery, state: FSMContext):
    if call.data == "request_menu":
        await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id,
                                    reply_markup=request_menu)
    else:
        select_all_requests = """SELECT * FROM comments WHERE dej IS NOT NULL and completed IS NOT 'yes' """
        all_requests = execute_read_query(connection, select_all_requests)
        button_list = []
        for i in all_requests:
            button_to_add = InlineKeyboardButton(f'{i[0]}', callback_data=f'{i[0]}')
            button_list.append(button_to_add)

        free_req_buttons = InlineKeyboardMarkup(
            inline_keyboard=[
                                button_list,
                                [InlineKeyboardButton('Вернуться в меню заявок', callback_data='request_menu')]
                            ]

        )
        await state.update_data(var=call.data)
        await Order_request_menu.wait_for_choose.set()
        await bot.edit_message_text('Список заявок в работе', call.from_user.id,
                                    call.message.message_id, reply_markup=free_req_buttons)


async def choosen_request(call: types.CallbackQuery, state: FSMContext):
    if call.data == "request_menu":
        await state.finish()
        await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id,
                                    reply_markup=request_menu)
    else:
        from sql import execute_read_query_with_par
        select_request = """SELECT * FROM comments WHERE id = (?)"""
        selected_request = execute_read_query_with_par(connection, select_request, (call.data,))
        my_data = await state.get_data()
        print('prishli suda')

        if my_data["var"] == 'free_requests':
            await bot.edit_message_text(f'Информация по заявке:\n{bot_defs.list_request(selected_request, "full")}',
                                        call.from_user.id, call.message.message_id, reply_markup=to_do_with_req_free)
        elif my_data["var"] == 'taken_requests':
            await bot.edit_message_text(f'Информация по заявке:\n{bot_defs.list_request(selected_request, "full")}',
                                        call.from_user.id, call.message.message_id, reply_markup=to_do_with_req_taken)
        elif my_data["var"] == 'archive_requests':
            await bot.edit_message_text(f'Информация по заявке:\n{bot_defs.list_request(selected_request, "full")}',
                                        call.from_user.id, call.message.message_id, reply_markup=to_do_with_req_archive)
        await state.update_data(req_id=call.data)
        await Order_request_menu.next()


async def take_req(call: types.CallbackQuery, state: FSMContext):
    from sql import execute_read_query_with_par
    my_data = await state.get_data()
    add_dej_to_request = """UPDATE comments SET dej = (?), dej_name = (?) WHERE id = (?)"""
    execute_query(connection, add_dej_to_request,
                  [(call.from_user.id, call.from_user.username, int(my_data["req_id"]))])
    select_request_to_anounce = """SELECT * FROM comments WHERE id = (?)"""
    selected_request_to_anounce = execute_read_query_with_par(connection,
                                                              select_request_to_anounce, (int(my_data["req_id"]),))
    await bot.send_message(selected_request_to_anounce[0]["telegram_id"],
                           f"Вашей заявкой №{selected_request_to_anounce[0]['id']}" 
                           f" начал заниматься {call.from_user.username}")
    await state.finish()
    await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id, reply_markup=request_menu)
    await call.answer("Вы взяли заявку в работу, пользователь получил уведомление", show_alert=True)

    """Формирование post для 1С"""
    select_dej_longphone = """SELECT * FROM admins WHERE telegram_name = (?)"""
    selected_dej_longphone = execute_read_query_with_par(connection, select_dej_longphone, (call.from_user.username,))
    import requests
    url = "http://mg.softbalance.ru:222/softbalance/hs/SDBot/"
    json_example = {
        "ExecutorNumber": selected_dej_longphone[0]['long_number'],
        "ClientNumber": selected_request_to_anounce[0]['phone_number'],
        "TaskTopic": f"Задача из телеграм бота номер {selected_request_to_anounce[0]['id']}",
        "TaskUrgency": "fast",
        "TaskDescription": f"{selected_request_to_anounce[0]['user_text']}"
    }

    print(json_example)
    resp = requests.post(url, json=json_example, auth=("SDbot", "159730"))
    # resp = requests.post(url, data=test_string, auth=('SDbot', '159730'))
    print(resp.status_code)
    print('post отправлен успешно')


async def del_req(call: types.CallbackQuery, state: FSMContext):
    my_data = await state.get_data()
    select_req_to_del = """DELETE FROM comments WHERE id = (?)"""
    execute_query(connection, select_req_to_del, [(int(my_data["req_id"]),)])
    await call.answer(f"Заявка номер {my_data['req_id']} удалена", show_alert=True)
    await bot.edit_message_text('Меню заявок', call.from_user.id, call.message.message_id, reply_markup=request_menu)
    await state.finish()


async def complete_req(call: types.CallbackQuery, state: FSMContext):
    to_del = await bot.edit_message_text('С каким комментарием закрываешь заявку?(пиши в чат)',
                                         call.from_user.id, call.message.message_id)
    await state.update_data(to_del=to_del.message_id)
    await Order_request_menu.next()


async def wait_for_completed_comment(message: types.Message, state: FSMContext):
    from sql import execute_read_query_with_par
    my_data = await state.get_data()
    await bot.delete_message(message.from_user.id, my_data["to_del"])
    select_req_to_complete = """UPDATE comments SET completed = (?),
     dej = (?), completed_comment = (?) WHERE id = (?)"""
    execute_query(connection, select_req_to_complete, [('yes',
                                                        message.from_user.id, message.text, int(my_data['req_id']))])
    select_request_to_anounce = """SELECT * FROM comments WHERE id = (?)"""
    selected_request_to_anounce = execute_read_query_with_par(connection,
                                                              select_request_to_anounce, (int(my_data["req_id"]),))
    await bot.send_message(selected_request_to_anounce[0]["telegram_id"],
                           f"{message.from_user.username} Закончил выполнение заявки"
                           f" №{selected_request_to_anounce[0]['id']}\nС комментарием: {message.text}")
    await bot.send_message(message.from_user.id, 'Заявку закрыл, вернул в меню заявок', reply_markup=request_menu)
    await bot.delete_message(message.from_user.id, message.message_id)
    await state.finish()


"""Изменение таймингов"""
timers_list_trigger = ['update_timer', 'priory_timer', 'alert_timer', 'alerts_is']


async def dea_alerts_220(call: types.CallbackQuery):
    dea_alerts_220_query = """UPDATE alerts_220 SET active = ? WHERE active = ?"""
    execute_query(connection, dea_alerts_220_query, [("no", "yes")])
    await call.answer("Алерты по падению электричества сброшены", show_alert=True)
    await bot.send_message(chat_id, f"Сотрудник {call.from_user.username} среагировал на отключение электроэнергии")


async def bot_settings_men_update_timer(call: types.CallbackQuery):
    await bot.edit_message_text('Выбери частоту обновления', call.from_user.id, call.message.message_id,
                                reply_markup=bot_settings_menu_update_timer)


async def bot_settings_men_alert_timer(call: types.CallbackQuery):
    await bot.edit_message_text('Выбери частоту обновления', call.from_user.id, call.message.message_id,
                                reply_markup=bot_settings_menu_alert_timer)


async def bot_settings_men_priory_timer(call: types.CallbackQuery):
    await bot.edit_message_text('Выбери частоту обновления', call.from_user.id, call.message.message_id,
                                reply_markup=bot_settings_menu_priory_timer)


async def bot_settings_men_alerts_is_active(call: types.CallbackQuery):
    await bot.edit_message_text('Активируй или декативируй бота', call.from_user.id, call.message.message_id,
                                reply_markup=bot_settings_menu_active_yes_no)


async def list_server_men(call: types.CallbackQuery):
    await bot.edit_message_text('Список каких серверов Вам интересен?', call.from_user.id, call.message.message_id,
                                reply_markup=list_server_menu)


async def choose_update_timer(call: types.CallbackQuery):
    bot_settings.update_settings(call.data.split()[0], call.data.split()[1])
    settings_list = bot_settings.read_settings_all()
    await bot.edit_message_text(f"Изменения приняты\n\n"
                                f"Пинги отрабатывают каждые {settings_list['update_timer']} секунд\n"
                                f"Алерты отправляются каждые {settings_list['alert_timer']} секунд\n"
                                f"Переход алертов на другого сотрудника в течении"
                                f" {settings_list['priory_timer']} секунд\n"
                                f"Оповещения работают: {settings_list['alerts_is_active']}",
                                call.from_user.id, call.message.message_id,
                                reply_markup=bot_settings_menu)


"""Добавление сервера в БД servers_to_ping"""
add_btn_stage_chose_rare = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Сервер со статусом Major', callback_data='major'),
                            InlineKeyboardButton('Сервер со статусом Secondary', callback_data='secondary'),
                            InlineKeyboardButton('Сервер со статусом Common', callback_data='common')
                        ]
                    ]
)

add_btn_stage_0 = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Да, добавляем', callback_data='uveren'),
                            InlineKeyboardButton('Нет, давай не будем', callback_data='btnDejmenu')
                        ]
                    ]
)


class AddServer(StatesGroup):
    waiting_for_request_name = State()
    waiting_for_request_rare = State()
    waiting_for_request_approve = State()


async def add_server(call: types.CallbackQuery, state: FSMContext):
    await bot.edit_message_text('Отправь мне название сервера или его IP адрес\nНапример sb-reso или '
                                '192.168.65.21', call.from_user.id, call.message.message_id)
    await AddServer.waiting_for_request_name.set()
    await state.update_data(to_del=call.message.message_id)


async def recieved_server_name(message: types.Message, state: FSMContext):
    request_data = await state.get_data()

    if not (re.match("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", message.text)
            or re.match("([a-zA-Z]{1,10}\-[a-zA-Z]{1,10})", message.text)):
        try:
            await bot.edit_message_text('Неверно введены данные\n'
                                        'Используй формат ip или dns: 192.168.77.77 или sb-reso ',
                                        message.chat.id, request_data['to_del'])
            await bot.delete_message(message.from_user.id, message.message_id)
        except:
            await bot.delete_message(message.from_user.id, message.message_id)
    else:
        await state.update_data(server_name=str(message.text))
        await message.delete()
        await bot.delete_message(message.chat.id, request_data['to_del'])
        await message.answer(f'Ты собираешься добавить сервер {message.text}', reply_markup=add_btn_stage_chose_rare)
        await AddServer.next()


async def recieved_server_rare(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(server_rare=str(call.data))
    request_data = await state.get_data()
    await bot.edit_message_text(f"Ты собираешься добавить сервер {request_data['server_name']} со "
                                f"статусом {request_data['server_rare']}",
                                call.from_user.id, call.message.message_id, reply_markup=add_btn_stage_0)
    await AddServer.next()


async def recieved_server_add_approve(call: types.CallbackQuery, state: FSMContext):
    if str(call.data) == 'btnDejmenu':
        await state.finish()
        await bot.edit_message_text('Меню дежурного', call.from_user.id, call.message.message_id,
                                    reply_markup=server_menu)
    else:
        request_data = await state.get_data()
        add_server_to_db = """
        INSERT INTO
            servers_to_ping (name, rare)
        VALUES
            (?,?)        
        """
        execute_query(connection, add_server_to_db, [(request_data['server_name'], request_data['server_rare'])])
        await bot.edit_message_text(f'Сервер {request_data["server_name"]} со статусом {request_data["server_rare"]} '
                                    f' добавлен в общий список серверов\n Вернул Вас в меню дежурного',
                                    call.from_user.id, call.message.message_id, reply_markup=server_menu)
        await state.finish()

"""Удаление сервера из БД servers_to_ping"""


class Order_removeServer(StatesGroup):
    wait_for_choose = State()
    wait_for_aprove = State()


remove_server_yes_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton('Да, удаляем', callback_data='uveren'),
            InlineKeyboardButton('Нет, давай не будем', callback_data='server_menu')
        ]

    ]
)


async def remove_server(call: types.CallbackQuery):
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    with open(pikserver, 'rb') as f:
        servers_status = pickle.load(f)
    button_list = []
    for i in servers_status:
        button_to_add = InlineKeyboardButton(f'{i.name}', callback_data=f'{i.name}')
        button_list.append(button_to_add)
    button_list.append(InlineKeyboardButton('Вернуться в меню серверов', callback_data='server_menu'))
    buttons_server = InlineKeyboardMarkup(row_width=2)
    for i in button_list:
        buttons_server.row(i)
        await bot.edit_message_text('Какой сервер удаляем?', call.from_user.id, call.message.message_id,
                                    reply_markup=buttons_server)
    await Order_removeServer.wait_for_choose.set()


async def server_to_remove_choosed(call: types.CallbackQuery, state: FSMContext):
    if str(call.data) == 'server_menu':
        await state.finish()
        await bot.edit_message_text('Меню управления серверами', call.from_user.id, call.message.message_id,
                                    reply_markup=server_menu)
    else:
        await state.update_data(server_to_remove=str(call.data))
        await bot.edit_message_text(f'Вы собираетесь удалить сервер {str(call.data)}\nУверены?',
                                    call.from_user.id, call.message.message_id, reply_markup=remove_server_yes_no)
        await Order_removeServer.next()


async def server_to_remove_approved(call: types.CallbackQuery, state: FSMContext):
    if str(call.data) == 'server_menu':
        await state.finish()
        await bot.edit_message_text('Меню управления серверами', call.from_user.id,
                                    call.message.message_id, reply_markup=server_menu)
    else:
        my_data = await state.get_data()
        pikserver = "/projects/sb_bot/data/pikserver.dat"
        with open(pikserver, 'rb') as f:
            servers_status = pickle.load(f)
            for i in servers_status:
                print(str(i.name) + ' == ' + str(my_data['server_to_remove']))
                if str(i.name) == (my_data['server_to_remove']):
                    print(f'udalyaem : {str(i.name)}')
                    servers_status.remove(i)
        with open(pikserver, 'wb') as f_1:
            pickle.dump(servers_status, f_1)

        delete_server_from_db_ping = """DELETE FROM servers_to_ping WHERE name = (?)"""
        execute_query(connection, delete_server_from_db_ping, ([(my_data["server_to_remove"],)]))
        delete_server_from_db_status = """DELETE FROM servers_status WHERE name = (?)"""
        execute_query(connection, delete_server_from_db_status, ([(my_data["server_to_remove"],)]))

        await bot.edit_message_text(f'Вы успешно удалили сервер {my_data["server_to_remove"]}\n'
                                    f'Я перестаю следить за его статусом, он больше '
                                    f'не отображается в списке серверов '
                                    f':( ', call.from_user.id, call.message.message_id, reply_markup=server_menu)
        await state.finish()

"""Заявка пользователя"""
stage_0 = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Компьютер', callback_data='Сломался компьютер'),
                            InlineKeyboardButton('Сервер', callback_data='Сломался сервер')

                        ],
                        [
                            InlineKeyboardButton('Другая проблема', callback_data='Сломалось что то другое')
                        ],
                        [
                            InlineKeyboardButton('Отменить заявку, вернуться в меню',
                                                 callback_data='level_0', state=None)
                        ]
                    ],

)
stage_1 = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Срочно', callback_data='Нужно очень срочно'),
                            InlineKeyboardButton('Не горит, подожду!', callback_data='Не горит, подожду')
                        ],
                        [
                            InlineKeyboardButton('Отменить заявку, вернуться в меню',
                                                 callback_data='level_0', state=None)
                        ]
                    ]
)
stage_2 = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Отменить заявку, вернуться в меню',
                                                 callback_data='level_0', state=None)
                        ],

                    ]
)


stage_3 = InlineKeyboardMarkup(
    inline_keyboard=[
                        [
                            InlineKeyboardButton('Отправить заявку дежурному',
                                                 requests_contact=True, callback_data='Send_request')
                        ],
                        [
                            InlineKeyboardButton('Изменить текст проблемы', callback_data='edit_text')
                        ],
                        [
                            InlineKeyboardButton('Отменить заявку, вернуться в меню', callback_data='level_0')
                        ]
                    ]
)


class OrderRequest(StatesGroup):
    waiting_for_request_problem = State()
    waiting_for_request_hury = State()
    waiting_for_request_text = State()
    waiting_for_request_phone = State()
    waiting_for_request_sent = State()


async def choose_problem(call: types.callback_query):
    await bot.edit_message_text('Выберите, что  у Вас сломалось', call.from_user.id,
                                call.message.message_id, reply_markup=stage_0)
    await OrderRequest.waiting_for_request_problem.set()


async def choosen_problem(call: types.callback_query, state: FSMContext):
    await state.update_data(problem=str(call.data))
    if str(call.data) == 'level_0':
        await state.finish()
        await bot.edit_message_text('Меню сотрудника', call.from_user.id,
                                    call.message.message_id, reply_markup=third_menu)
    else:
        await OrderRequest.next()
        await bot.edit_message_text('Как срочно Вам нужна помощь?',
                                    call.from_user.id, call.message.message_id, reply_markup=stage_1)


async def choosen_hury(call: types.callback_query, state: FSMContext):
    await state.update_data(to_delete=call.message.message_id)
    await state.update_data(hury=str(call.data))
    if str(call.data) == 'level_0':
        await state.finish()
        await bot.edit_message_text('Меню сотрудника', call.from_user.id,
                                    call.message.message_id, reply_markup=third_menu)
    else:
        await OrderRequest.next()
        await bot.edit_message_text('Отправьте мне сообщение с кратким описание проблемы..\n'
                                    '(Пиши в чат )',
                                    call.from_user.id, call.message.message_id, reply_markup=stage_2)


async def decline_request(call: types.CallbackQuery, state: FSMContext):
    if str(call.data) == 'level_0':
        await state.finish()
        await bot.edit_message_text('Меню сотрудника', call.from_user.id,
                                    call.message.message_id, reply_markup=third_menu)


async def choosen_text(message: types.Message, state: FSMContext):
    req_data = await state.get_data()
    share_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    share_button = types.KeyboardButton(text="\U0000260E Отправить боту свой"
                                             " номер телефона \U0000260E", request_contact=True)
    share_keyboard.add(share_button)

    await state.update_data(text=message.text)
    await state.update_data(my_chat_id=message.chat.id)
    await bot.delete_message(message.chat.id, message.message_id)
    to_del = await message.answer("Чтобы сотрудник SD смог с тобой связаться - \nоставь нам свои контакты.\n\n"
                                  "Либо напиши в чат, например:   Иванов Иван 89217772345\n"
                                  "Но лучше просто нажми кнопку с значком \U0000260E внизу экрана",
                                  reply_markup=share_keyboard)
    await state.update_data(to_del=to_del.message_id)
    await OrderRequest.next()
    await bot.delete_message(message.chat.id, req_data['to_delete'])


async def choose_phone_v2(message: types.Message, state: FSMContext):
    req_data = await state.get_data()
    if message.text == '/start':
        await state.finish()
        await bot.delete_message(message.from_user.id, req_data['to_del'])
        await bot.send_message(message.from_user.id, 'Главном меню.\n', reply_markup=main_menu)

    if not re.match("([a-zA-Zа-яА-Я]{1,10}\s[a-zA-Zа-яА-Я]{1,10}\s\d{1,14})", message.text):
        try:
            await bot.edit_message_text('Неверно введены данные\n'
                                        'Используй формат : Имя Фамилия 89217772345',
                                        message.chat.id, req_data['to_del'])
            await bot.delete_message(message.from_user.id, message.message_id)
        except Exception as e:
            print(e)
            await bot.delete_message(message.from_user.id, message.message_id)
    else:
        await state.update_data(phone_to_call=message.text.split()[2])
        await state.update_data(member_first_name=message.text.split()[1])
        await state.update_data(member_last_name=message.text.split()[0])
        req_data = await state.get_data()
        await bot.delete_message(message.chat.id, req_data['to_del'])
        await bot.delete_message(message.chat.id, message.message_id)
        await bot.send_message(message.chat.id, f'Давайте проверим Вашу заявку перед отправкой:\n\n'
                                                f'Что сломалось: {req_data["problem"]}\n'
                                                f'Как срочно нужно сделать: {req_data["hury"]}\n'
                                                f'Описание проблемы: {req_data["text"]}\n'
                                                f'Данные для обратной связи: {req_data["phone_to_call"]}\n'
                                                f'Как к Вам обращаться: {req_data["member_first_name"]}'
                                                f' {req_data["member_last_name"]}', reply_markup=stage_3)
        await OrderRequest.next()


async def choosen_phone(message: types.ContentType.CONTACT, state: FSMContext):
    await state.update_data(phone_to_call=message.contact.phone_number)
    await state.update_data(member_first_name=message.contact.first_name)
    await state.update_data(member_last_name=message.contact.last_name)
    req_data = await state.get_data()
    await bot.delete_message(message.chat.id, req_data['to_del'])
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, f'Давайте проверим Вашу заявку перед отправкой:\n\n'
                                            f'Что сломалось: {req_data["problem"]}\n'
                                            f'Как срочно нужно сделать: {req_data["hury"]}\n'
                                            f'Описание проблемы: {req_data["text"]}\n'
                                            f'Данные для обратной связи: {req_data["phone_to_call"]}\n'
                                            f'Как к Вам обращаться: {req_data["member_first_name"]}'
                                            f' {req_data["member_last_name"]}', reply_markup=stage_3)
    await OrderRequest.next()


async def sent(call: types.CallbackQuery, state: FSMContext):
    if str(call.data) == 'level_0':
        await state.finish()
        await bot.edit_message_text('Меню сотрудника', call.from_user.id,
                                    call.message.message_id, reply_markup=third_menu)
    elif str(call.data) == 'edit_text':
        my_data = await state.get_data()
        await OrderRequest.waiting_for_request_text.set()
        await state.update_data(to_delete=call.message.message_id)
        await bot.edit_message_text(f'Окей, давайте перезапишем ваше сообщение. Вот что вы написали:\n{my_data["text"]}',
                                    call.from_user.id, call.message.message_id, reply_markup=stage_2)
    else:
        my_data = await state.get_data()
        pikperson = "/projects/sb_bot/data/pikperson.dat"
        with open(pikperson, 'rb') as f:
            spisok_adminov = pickle.load(f)
        dejurniy = bot_defs.choose_dej(spisok_adminov)
        await state.finish()
        await bot.edit_message_text('Ваше обращение отправлено дежурному, он свяжется с Вами в ближайшее время.'
                                    '\nВернул Вас в меню пользователя.',
                                    call.from_user.id, call.message.message_id, reply_markup=third_menu)

        add_new_request = """
                            INSERT INTO 
                                comments (phone_number, telegram_id, user_text, admin_text)
                            VALUES
                                (?,?,?,?)
                          """
        execute_query(connection, add_new_request, ([(my_data['phone_to_call'], call.from_user.id,
                                                      f"Что сломалось: {my_data['problem']}\n"
                                                      f"Как срочно нужно помочь: {my_data['hury']}\n"
                                                      f"Краткое описание проблемы: {my_data['text']}\n",
                                                      f"Кто попросил о помощи: {call.from_user.username}\n"
                                                      f"Его контактный номер телефона: {my_data['phone_to_call']}\n"
                                                      f"Его фамилия и имя: {my_data['member_first_name']}"
                                                      f"{my_data['member_last_name']}\n\n")]))
        await bot.send_message(chat_id, f'Поступила заявка от пользователя:\n'
                                        f'Что сломалось: {my_data["problem"]}\n'
                                        f'Как срочно нужно помочь: {my_data["hury"]}\n'
                                        f'Краткое описание проблемы: {my_data["text"]}\n'
                                        f'Кто попросил о помощи: {call.from_user.username}\n'
                                        f'Его контактный номер телефона: {my_data["phone_to_call"]}\n'
                                        f'Его фамилия и имя: {my_data["member_first_name"]}'
                                        f' {my_data["member_last_name"]}')


async def exit_from_bot(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Всего доброго! \n\nНо если вдруг надумаешь вернуться - пиши /start')


def register_handlers_client(dp: Dispatcher):
    """команды старта"""
    dp.register_message_handler(level_0_0, commands='start', state='*')

    """Регистрация сотрудника SD"""
    dp.register_message_handler(sd_key, commands='reg')
    dp.register_callback_query_handler(level_0, text='i_ladno')
    dp.register_message_handler(sd_fio, state=Order_sd.waiting_for_key)
    dp.register_message_handler(sd_priory, state=Order_sd.waiting_for_fio)
    dp.register_callback_query_handler(sd_phone, state=Order_sd.waiting_for_priory)
    dp.register_message_handler(sd_complete, state=Order_sd.waiting_for_phone)
    dp.register_callback_query_handler(sd_accept, state=Order_sd.waiting_for_accept)

    """Создание заявки"""
    dp.register_callback_query_handler(level_0, text='level_0')
    dp.register_callback_query_handler(choosen_problem, state=OrderRequest.waiting_for_request_problem)
    dp.register_callback_query_handler(choosen_hury, state=OrderRequest.waiting_for_request_hury)
    dp.register_callback_query_handler(decline_request, state=OrderRequest.waiting_for_request_text)
    dp.register_message_handler(choosen_text, state=OrderRequest.waiting_for_request_text)
    dp.register_message_handler(choose_phone_v2, state=OrderRequest.waiting_for_request_phone)
    dp.register_message_handler(choosen_phone, state=OrderRequest.waiting_for_request_phone,
                                content_types=types.ContentType.CONTACT)
    dp.register_callback_query_handler(sent, state=OrderRequest.waiting_for_request_sent)

    """Команды меню"""
    dp.register_callback_query_handler(third_men, text='btnUsermenu')
    dp.register_callback_query_handler(list_all_sd, text='list_all_sd')
    dp.register_callback_query_handler(list_today_dejurniy, text='who_is_dejurniy?')
    dp.register_callback_query_handler(choose_problem, text='make_request')
    dp.register_callback_query_handler(randoms, text='btnRandom')
    dp.register_callback_query_handler(exit_from_bot, text='btnExit')
    dp.register_callback_query_handler(dej_spisok, text='dej_spisok')
    dp.register_callback_query_handler(sotr_spisok, text='sotr_spisok')
    dp.register_callback_query_handler(list_my_requests, text='my_requests')

    """После этого хендлера блок на команды пользователя"""
    dp.register_callback_query_handler(handle_unwanted_users, lambda call: call.from_user.id not in check_adm())

    """Меню дежурного"""
    dp.register_callback_query_handler(second_men, text='btnDejmenu')
    dp.register_callback_query_handler(server_men, text='server_menu')
    dp.register_callback_query_handler(choose_update_timer,
                                       lambda call: any(s in call.data for s in timers_list_trigger))
    dp.register_callback_query_handler(dea_alerts_220, text='dea_alert_220')
    dp.register_callback_query_handler(bot_settings_men_update_timer, text='change_server_time_to_ping')
    dp.register_callback_query_handler(bot_settings_men_alert_timer, text='change_alert_time')
    dp.register_callback_query_handler(bot_settings_men_priory_timer, text='change_next_time')
    dp.register_callback_query_handler(bot_settings_men_alerts_is_active, text='switch_on_off_bot_alerts')
    dp.register_callback_query_handler(bot_settings_men, text='bot_settings')
    dp.register_callback_query_handler(list_servers_with_category, text=['major', 'secondary', 'down', 'common'])
    dp.register_callback_query_handler(list_server_men, text='list_server_menu')
    dp.register_callback_query_handler(register_in_bot, text='register_in_bot')
    dp.register_callback_query_handler(inwork_spisok, text='inwork_spisok')

    """Меню заявок"""
    dp.register_callback_query_handler(req_menu, text='request_menu')
    dp.register_callback_query_handler(archive_req, text='archive_requests')
    dp.register_callback_query_handler(free_req, text='free_requests')
    dp.register_callback_query_handler(taken_req, text='taken_requests')
    dp.register_callback_query_handler(choosen_request, state=Order_request_menu.wait_for_choose)
    dp.register_callback_query_handler(req_menu, text='request_menu', state=Order_request_menu.wait_for_action)
    dp.register_callback_query_handler(take_req, text='take_request', state=Order_request_menu.wait_for_action)
    dp.register_callback_query_handler(del_req, text='delete_request', state=Order_request_menu.wait_for_action)
    dp.register_callback_query_handler(complete_req, text='complete_request', state=Order_request_menu.wait_for_action)
    dp.register_message_handler(wait_for_completed_comment, state=Order_request_menu.wait_for_action_complete)
    """Добавление сервера"""
    dp.register_callback_query_handler(add_server, text='add_server')
    dp.register_message_handler(recieved_server_name, state=AddServer.waiting_for_request_name)
    dp.register_callback_query_handler(recieved_server_rare, state=AddServer.waiting_for_request_rare)
    dp.register_callback_query_handler(recieved_server_add_approve, state=AddServer.waiting_for_request_approve)

    """Удаление сервера"""
    dp.register_callback_query_handler(remove_server, text='remove_server')
    dp.register_callback_query_handler(server_to_remove_choosed, state=Order_removeServer.wait_for_choose)
    dp.register_callback_query_handler(server_to_remove_approved, state=Order_removeServer.wait_for_aprove)
