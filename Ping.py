"""Проверка доступности серверов"""

import asyncio
import sys
import async_timeout
import pickle
from sql import connection, execute_read_query, execute_query

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def sortservers():
    from classServer import Server_data
    import datetime

    alerts_count = []
    g = 0
    times_alert_number = 0

    select_from_server_status = """SELECT * from servers_status"""
    servers_from_status = execute_read_query(connection, select_from_server_status)
    pikserver = "/projects/sb_bot/data/pikserver.dat"
    with open(pikserver, 'rb') as f:
        all_servers_list = pickle.load(f)

    select_from_servers_to_ping = """SELECT * from servers_to_ping"""
    servers_from_ping = execute_read_query(connection, select_from_servers_to_ping)

    """забираем имя и статус сервера из свежей выборки, создаем объект сервера"""
    for i in servers_from_status:

        new_name = i["name"]
        new_status = i["status"]

        alerts_count.append(new_name)
        alerts_count[g] = Server_data(new_name, new_status)

        for t in servers_from_ping:
            h = t["rare"]
            if t["name"] == new_name:
                new_rare = h
                alerts_count[g].rare = new_rare

        if alerts_count[g].status == 'DOWN':
            alerts_count[g].oborot = str(u'\U0001F534')
            alerts_count[g].when_down = datetime.datetime.now().time()
            alerts_count[g].when_down_present = datetime.datetime.now().strftime("%d.%b, %Y, %H:%M:%S")
        else:
            alerts_count[g].oborot = str(u'\U0001F7E2')

        for k in all_servers_list:
            if k.name == alerts_count[g].name and alerts_count[g].status == 'DOWN':
                times_alert_number = times_alert_number + 1
                alerts_count[g].alert_number = times_alert_number
                alerts_count[g].who_took = k.who_took
                alerts_count[g].active = k.active
                alerts_count[g].rare = k.rare
                if k.when_down != datetime.datetime(1, 1, 1, 0, 0):
                    alerts_count[g].when_down = k.when_down
            elif k.name == alerts_count[g].name:
                k.rare = alerts_count[g].rare
        g = g + 1

    """убираем дубли алертов, оставляем верхние статусы"""
    all_servers_list = list(set(alerts_count+all_servers_list))

    with open(pikserver, 'wb') as f:
        pickle.dump(all_servers_list, f)


async def ping_server(server, timeout=3):
    import aioping
    try:
        async with async_timeout.timeout(timeout):
            fields = await aioping.ping(server["name"])
            if fields:
                print(f'{server["name"]} Server UP')
                add_server_up = """
                                    INSERT INTO
                                        servers_status (name, status)
                                    VALUES
                                        (?,?)
                                    ON CONFLICT(name) DO UPDATE SET
                                        name = excluded.name,
                                        status = 'UP'
                                """
                execute_query(connection, add_server_up, [(server["name"], "UP")])
    except:
        print(f'{server["name"]} Server Down- Alert')
        add_server_up = """
                                            INSERT INTO
                                                servers_status (name, status)
                                            VALUES
                                                (?,?)
                                            ON CONFLICT (name) DO UPDATE SET
                                                name = excluded.name,
                                                status = 'DOWN'
                                        """
        execute_query(connection, add_server_up, [(server["name"], "DOWN")])


async def main():
    select_users = """SELECT name from servers_to_ping"""
    host_list = execute_read_query(connection, select_users)
    tasks = [ping_server(host) for host in host_list]
    for future in asyncio.as_completed(tasks):
        await future
    await asyncio.sleep(0.1)
    sortservers()
    print('SYSTEM MSG: script "ping" completed')

if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(main())
