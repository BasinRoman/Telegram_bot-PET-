""" Вспомогательные функции для бота  """
import asyncio

import classServer
import datetime


def tab_list(my_list):
    times = ''
    counter = 0
    for i in my_list:
        counter = counter + 1
        server_info = str('\n' + str(counter) + ') ' + classServer.Server_data.show_server_status(i) + '\n')
        times = str(' ' + times + server_info)
    return times


def tab_list_major(my_list, rare):
    times_major = ''
    times_secondary = ''
    times_down = ''
    times_common = ''
    counter = 0

    for i in my_list:
        if i.rare == 'major':
            counter = counter + 1
            server_info = str('\n' + str(counter) + ') ' + classServer.Server_data.show_server_status(i) + '\n')
            times_major = str(' ' + times_major + server_info)
        if i.rare == 'secondary':
            counter = counter + 1
            server_info = str('\n' + str(counter) + ') ' + classServer.Server_data.show_server_status(i) + '\n')
            times_secondary = str(' ' + times_secondary + server_info)
        if i.rare == 'common':
            counter = counter + 1
            server_info = str('\n' + str(counter) + ') ' + classServer.Server_data.show_server_status(i) + '\n')
            times_common = str(' ' + times_common + server_info)
        if i.status == 'DOWN':
            counter = counter + 1
            server_info = str('\n' + str(counter) + ') ' + classServer.Server_data.show_server_status(i) + '\n')
            times_down = str(' ' + times_down + server_info)

    if rare == 'major':
        return times_major
    elif rare == 'secondary':
        return times_secondary
    elif rare == 'common':
        return times_common
    elif rare == 'down':
        return times_down


def list_request(my_requests, var):
    times = ''
    for x in my_requests:
        if x["completed"] == 'yes' and x["dej_name"]:
            dej = f'Заявка выполнена сотрудником {x["dej_name"]} \U00002705'
        elif x["completed"] == 'yes':
            dej = 'Заявка выполнена \U00002705'
        elif not x["dej_name"]:
            dej = 'Заявку еще не рассмотрели \U000026A0'
        elif x["dej_name"]:
            dej = f'Заявку выполняет сотрудник {x["dej_name"]} \U00002692'

        if var == 'user':
            times = str(times + str(f'Номер заявки {x["id"]}\nСтатус заявки: {dej}\n') +
                        f'Комментарий SD: {x["completed_comment"]}\n' + x["user_text"] + "\n")
        elif var == 'admin':
            times = str(times + str(f'Номер заявки {x["id"]}\nСтатус заявки: {dej}\n') + x["admin_text"] + "\n")
        elif var == 'full':
            times = str(times + str(f'Номер заявки {x["id"]}\nСтатус заявки: {dej}\n')
                        + x["user_text"] + x["admin_text"] + "\n")
    return times


def list_server(my_list):
    times = ''
    for i in my_list:
        times = str(' ' + times + classServer.Server_data.show_name_whotook(i) + '\n')
    return times


def list_person(my_list):
    times = ''
    counter = 0
    for i in my_list:
        counter = counter + 1
        person_info = classServer.Person.show_person(i)
        times = str(f"{times}{counter}) {person_info}\n")
    return times


def list_dej_calendar(my_list):
    times = ''
    for i in my_list:
        day_info = f"\n{i['day_number'].strftime('%d.%b, %Y')} {str(i['short_number'])} {str(i['telegram_name'])}"
        times = times + day_info
    return times


def choose_dej(my_list):
    for dejurniy in my_list:
        if dejurniy.is_dejurniy == 1:
            return dejurniy


async def get_today_dejurniy():
    import pickle
    from dejurnie import dejurnie
    today = datetime.date.today()

    def find_by_key(iterable, key, value):
        for index, dict_ in enumerate(iterable):
            if key in dict_ and dict_[key] == value:
                return dict_
    today_dej = find_by_key(dejurnie(), 'day_number', today)
    pikperson = "/projects/sb_bot/data/pikperson.dat"
    with open(pikperson, 'rb') as f:
        dejurniy = pickle.load(f)
    for i in dejurniy:
        if i.name == today_dej['name']:
            i.is_dejurniy = 1
        else:
            i.is_dejurniy = 0
    with open(pikperson, 'wb') as f:
        pickle.dump(dejurniy, f)
    # добавить обновление базы данных ?
    print(f"SYSTEM: piperson updated, dejurniy selected : {today_dej}")
    await asyncio.sleep(0)


async def update_pikperson_from_bd():
    from classServer import Person
    from sql import connection, execute_read_query
    import pickle

    select_from_admins = """SELECT * from admins"""
    admins_from_bd = execute_read_query(connection, select_from_admins)

    spisok_sotrudnikov_pik = '/projects/sb_bot/data/pikperson.dat'
    with open(spisok_sotrudnikov_pik, mode='rb') as j:
        times_spisok_sotrudnikov = pickle.load(j)

    person_list = []
    g = 0
    for i in admins_from_bd:
        name = i['name']
        telegram_name = i['telegram_name']
        telegram_id = i['telegram_id']
        short_number = i['short_number']
        long_number = i['long_number']
        priory = i['priory']
        is_dejurniy = i['is_dejurniy']
        person_list.append(name)
        person_list[g] = Person(name, short_number, long_number, telegram_name, priory, telegram_id, is_dejurniy)
        g = g + 1

    times_spisok_sotrudnikov = list(set(person_list + times_spisok_sotrudnikov))

    with open(spisok_sotrudnikov_pik, mode='wb') as g:
        pickle.dump(times_spisok_sotrudnikov, g)
    print('SYSTEM: pikperson updated from BD')
    await asyncio.sleep(0)

if __name__ == '__main__':
    print('hello world')
