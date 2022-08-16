import asyncio
import datetime
import pickle

import aioschedule
from aiogram.utils import executor

import Ping
import bot_defs
import get_email
from sql import connection, execute_read_query_with_par
from bot_settings import read_settings
from chat_ids import chat_id, chat_id_list
from create_bot import dp, bot
from handlers import other, client


async def morning_message():
    today = datetime.date.today()
    pikperson = "/projects/sb_bot/data/pikperson.dat"
    dejurniy_selected = False
    """выводим дежурного в этот день"""
    with open(pikperson, 'rb') as f:
        spisok_adminov = pickle.load(f)
    for chat_id in chat_id_list:
        if spisok_adminov:
            for admin in spisok_adminov:
                if admin.is_dejurniy == 1:
                    await bot.send_message(chat_id, f"Доброе утро!\n"
                                                    f"Сегодня {today}\n"
                                                    f"Дежурный в этот день {admin.name}\n"
                                                    f"Короткий номер сотрудника {admin.short_number}\n"
                                                    f"Мобильный номер {admin.long_number}\n"
                                                    f"Городской телефон  372-50-08", disable_notification=True)
                    dejurniy_selected = True
            if dejurniy_selected is False:
                await bot.send_message(chat_id, f"Доброе утро!\n"
                                                f"Сегодня {today}\n"
                                                f"По графику, сегодня нет дежурного.\n"
                                                f"Для помощи - можешь обратиться к любому сотруднику SD")
            """выводим список админов ( по желанию )"""
            # pikperson = "/projects/sb_bot/data/pikperson.dat"
            # with open(pikperson, 'rb') as f:
            #     spisok_adminov = pickle.load(f)
            # await bot.send_message(chat_id, bot_defs.list_person(spisok_adminov),
            #                        parse_mode="HTML", disable_web_page_preview=True)
        else:
            await bot.send_message(chat_id, 'Администраторы отсутствуют. Ожидаю, пока кто то из них зарегистрируется.')
        await asyncio.sleep(0.1)

async def alert_220():
    if read_settings('alerts_is_active') is True:
        select_yes_220 = """SELECT * FROM alerts_220 WHERE active = (?)"""
        selected_yes_220 = execute_read_query_with_par(connection, select_yes_220, ("yes",))
        if selected_yes_220:
            for i in selected_yes_220:
                await bot.send_message(chat_id, f"ВСЕМ СОТРУДНИКАМ ВНИМАНИЕ! В ОФИСЕ УПАЛО ЭЛЕКТРИЧЕСТВО НА"
                                                f" ПЕРВОМ ЭТАЖЕ {i['date']}")
async def down_alert():
    """Отправка алерта"""
    if read_settings('alerts_is_active') is True:
        check = True
        # Выставляем интервал, после которого алерт перейдет следующему по priory сотруднику
        time_step = read_settings('priory_timer')
        pikperson = "/projects/sb_bot/data/pikperson.dat"
        with open(pikperson, 'rb') as f:
            spisok_adminov = pickle.load(f)
            print(spisok_adminov)
        dejurniy = bot_defs.choose_dej(spisok_adminov)
        pikserver = "/projects/sb_bot/data/pikserver.dat"
        with open(pikserver, 'rb') as f:
            servers_status = pickle.load(f)

        for i in servers_status:
            if i.status == 'DOWN' and i.who_took == '' and i.active == 1:
                time_b = datetime.datetime.combine(datetime.date.today(), i.when_down)
                time_dif = (datetime.datetime.now() - time_b).total_seconds()
                priory = time_dif // time_step
                if time_dif < time_step:
                    if dejurniy:
                        if dejurniy.telegram_id == 0:
                            await bot.send_message(chat_id, f"Мне не хватает telegram_id сотрудника @{dejurniy.telegram_name}"
                                                            f"\n\n"
                                                            f"@{dejurniy.telegram_name} Как дежурный в этот день срочно "
                                                            f"подними сервер {i.name}\nЧтобы взять сервер в работу "
                                                            f"напиши в чат /take {i.alert_number}")
                        else:
                            await bot.send_message(dejurniy.telegram_id, f"Как дежурный в этот день"
                                                                         f" срочно подними сервер {i.name}\nЧтобы "
                                                                         f"взять сервер в работу напиши "
                                                                         f"в чат /take {i.alert_number}")
                elif time_dif > time_step:
                    for p in spisok_adminov:
                        if int(p.priory) == int(priory):
                            if dejurniy:
                                if p.telegram_name != dejurniy.telegram_name:
                                    if p.telegram_id == 0:
                                        await bot.send_message(chat_id, f"Мне не хватает айди сотрудника"
                                                                        f" {p.telegram_name}\n\n"
                                                                        f"@{p.telegram_name}"
                                                                        f" срочно подними сервер {i.name}\n"
                                                                        f"Напиши в чат /take {i.alert_number}\n")
                                    else:
                                        await bot.send_message(p.telegram_id, f"@{p.telegram_name}"
                                                                              f" срочно подними сервер {i.name}\n"
                                                                              f"Напиши в чат /take {i.alert_number}\n")
                                    check = False
                            else:
                                if p.telegram_id == 0:
                                    await bot.send_message(chat_id,
                                                           f"Дежурный не назначен!\nМне не хватает айди сотрудника"
                                                           f" {p.telegram_name}\n\n"
                                                           f"@{p.telegram_name} срочно подними сервер {i.name}\n"
                                                           f"Напиши в чат /take {i.alert_number}\n")
                                else:
                                    await bot.send_message(p.telegram_id,
                                                           f"Дежурный не назначен!\n@{p.telegram_name}"
                                                           f" срочно подними сервер {i.name}\n"
                                                           f"Напиши в чат /take {i.alert_number}\n")
                                check = False
                    if check is True:
                        await bot.send_message(chat_id, f'Это общий алерт, никто не взял сервер  в работу.'
                                                        f' Так что поднимаем всем отделом!\n{str(i)}\n'
                                                        f'Напиши в чат /take {i.alert_number}\n')
    else:
        print('SYSTEM MSG: alerts disabled, so i`m just chilling')


async def sheduler():
    """ Ночное обновление pikperson и сверка с БД """
    aioschedule.every().day.at('00:02').do(bot_defs.update_pikperson_from_bd)
    aioschedule.every().day.at('00:03').do(bot_defs.get_today_dejurniy)
    """ Утреннее приветствие """
    aioschedule.every().day.at('10:00').do(morning_message, )
    aioschedule.every(read_settings('alert_timer')).seconds.do(down_alert, )
    aioschedule.every(15).seconds.do(alert_220, )
    aioschedule.every(60).seconds.do(get_email.main, )
    aioschedule.every(read_settings('update_timer')).seconds.do(Ping.main, )
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(0.1)


async def on_startup(_):
    # await bot.send_message(chat_id, 'Бот запущен')
    await bot_defs.update_pikperson_from_bd()
    await bot_defs.get_today_dejurniy()
    asyncio.create_task((sheduler()))

client.register_handlers_client(dp)
other.register_handlers_client(dp)
executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
