# """  Проверка доступности серверов из почтового ящика по алертам (например Либры)  """
#
#
# async def sortServers():
#     import json, pickle
#     from classServer import Server_data
#     import datetime
#
#     """for test use inbox_emails_test.txt"""
#     inbox_emails = '/projects/sb_bot/data/inbox_emails.txt'
#     emails = open(inbox_emails, mode='r', encoding='utf-8')
#     alerts_count = []
#     g = 0
#     times_alert_number = 0
#
#     PIKserver = "/projects/sb_bot/data/PIKserver.dat"
#     with open(PIKserver, 'rb') as f:
#         all_servers_list = pickle.load(f)
#     Servers_to_ping = '/projects/sb_bot/data/Servers_to_ping.txt'
#     with open(Servers_to_ping, 'r') as s:
#         rare = s.readlines()
#
#     """забираем имя и статус сервера из свежей выборки, создаем объект сервера"""
#     for i in emails:
#         new_name = i.split()[0]
#         new_status = i.split()[2]
#         alerts_count.append(new_name)
#         alerts_count[g] = Server_data(new_name, new_status)
#
#         for t in rare:
#             h = t.split()[1]
#             if t.split()[0] == new_name:
#                 new_rare = h
#                 alerts_count[g].rare = new_rare
#
#         if alerts_count[g].status == 'Down':
#             alerts_count[g].oborot = str(u'\U0001F534')
#             alerts_count[g].when_down = datetime.datetime.now().time()
#             alerts_count[g].when_down_present = datetime.datetime.now().strftime("%d.%b, %Y, %H:%M:%S")
#
#         else:
#             alerts_count[g].oborot = str(u'\U0001F7E2')
#
#         for k in all_servers_list:
#             if k.name == alerts_count[g].name and alerts_count[g].status == 'Down':
#                 times_alert_number = times_alert_number + 1
#                 alerts_count[g].alert_number = times_alert_number
#                 alerts_count[g].who_took = k.who_took
#                 alerts_count[g].active = k.active
#                 alerts_count[g].rare = k.rare
#                 if k.when_down != datetime.datetime(1, 1, 1, 0, 0):
#                     alerts_count[g].when_down = k.when_down
#             elif k.name == alerts_count[g].name:
#                 k.rare = alerts_count[g].rare
#         g = g + 1
#
#     """убираем дубли алертов, оставляем верхние статусы"""
#     all_servers_list = list(set(alerts_count+all_servers_list))
#
#     with open('/projects/sb_bot/data/servers.json', 'w', encoding='utf-8') as f:
#         json.dump(all_servers_list, f, ensure_ascii=False, indent=4, default=str)
#
#     with open(PIKserver, 'wb') as f:
#         pickle.dump(all_servers_list, f)
#     print('sort_server_otrabotal')
#     emails.close()
#
# if __name__ == '__main__':
#     print('hello world')
