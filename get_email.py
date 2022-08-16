
""" Функция собирает алерты из почтового ящика и помещает их в БД """
import asyncio
from credentials import email_login, email_password, email_server, primary_smtp_address


async def get_emails():
    i = 0
    from exchangelib import Credentials, Account, Configuration, DELEGATE
    import asyncio
    from sql import execute_query, connection

    credentials = Credentials(username=f"{email_login}", password=f"{email_password}")
    config = Configuration(server=f'{email_server}', credentials=credentials)
    account = Account(primary_smtp_address=f'{primary_smtp_address}', autodiscover=False, config=config,
                      access_type=DELEGATE)
    alert_folder = account.root / 'Корневой уровень хранилища' / 'Входящие'
    while (True and i<1):
        try:
            import pytz
            from exchangelib import EWSDateTime, EWSTimeZone, UTC_NOW, Q
            from datetime import datetime, timedelta

            inbox_emails = '/projects/sb_bot/data/inbox_emails.txt'
            emails = open(inbox_emails, mode='w', encoding='utf-8')
            current_date = datetime.now(pytz.utc)
            start_date = datetime(2022,4,10)
            start_date = start_date.replace(tzinfo=pytz.utc)
            since = UTC_NOW() - timedelta(hours=90)
            q = (
                Q(subject__icontains=('eaton5000@softbalance.ru')) | Q(subject__icontains=('9135'))
                )
            # q - any filter you wish to search by subject
            myfilter = alert_folder.filter(q) \
                .exclude(subject__contains="ANYMARKHERE") \
                .exclude(subject__contains="SNMP") \
                .filter(datetime_received__gte=since)\
                .order_by('-datetime_received')
            new_alerts = ()
            for item in myfilter:
                i = i + 1
                print(i)
                new_alert = str(item.datetime_received)
                print(new_alert)
                activate_220_allert = """INSERT INTO alerts_220 (date) VALUES (?) ON CONFLICT(date) DO NOTHING"""
                execute_query(connection, activate_220_allert, [(new_alert,)])

            i = i + 1
            emails.close()

            await asyncio.sleep(0.1)
        except:
            await asyncio.sleep(0.1)
            import time
            return


async def main():
    tasks = [get_emails()]
    for future in asyncio.as_completed(tasks):
        await future
    await asyncio.sleep(0.1)
    print('SYSTEM MSG: script GET_EMAIL completed')
if __name__ == '__main__':
    event_loop = asyncio.new_event_loop()
    event_loop.run_until_complete(main())
"""вызов функции для теста"""
# asyncio.run(get_emails())
# print('Function get_emails completed')
"""***********************"""
