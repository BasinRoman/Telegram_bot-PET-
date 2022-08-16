"""Класс сервера"""

import datetime


class Server_data:
    def __init__(self, name, status):
        self.name = name
        self.status = status
        self.oborot = ''
        self.alert_number = 0
        self.who_took = ''
        self.when_down = datetime.datetime(1, 1, 1, 0, 0)
        self.when_down_present = datetime.datetime(1, 1, 1, 0, 0)
        self.priory = 0
        self.active = 1
        self.rare = ' '

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return format(f"{self.name} {self.status} {self.oborot} {str(self.alert_number)} "
                      f"{str(self.when_down)} {str(self.rare)}")
        # return format(self.name)

    def __json__(self):
        return self.__dict__

    def show_server_status(self):
        # Для отображения полной информации в /servers  - используй этот status
        # status = (' name = ' + str(self.name) + '\n    status = ' + str(self.status) + '  ' + str(self.oborot) +
        #           '\n     Порядковый номер алерта =' + str(self.alert_number) + '\n     сейчас в работе за ' +
        #           str(self.who_took) + '\n     сервер упал в = ' + str(self.when_down))
        if self.status == 'Down':
            if self.who_took == '':
                status = (' Имя сервера  ' + str(u'\U00002796' + ' ') + str(self.name) + '\n      Статус сервера ' +
                          str(u'\U00002796' + ' ') + str(self.status) + '  ' + str(self.oborot) +
                          '\n      Порядковый номер алерта ' + str(u'\U00002796' + ' ') + str(self.alert_number) +
                          '\n      сейчас в работе за ' + str(u'\U00002796' + ' ')
                          + 'Никто не взял сервер в работу' + '\n      сервер упал в ' + str(u'\U00002796' + ' ') +
                          str(self.when_down_present) + '\n      Алерты сервера активированы ' +
                          str(u'\U00002796' + ' ') + str(self.active) + '\n      Важность сервера ' + str(self.rare))
            else:
                status = (' Имя сервера ' + str(u'\U00002796' + ' ') + str(self.name) + '\n      Статус сервера ' +
                          str(u'\U00002796' + ' ') + str(self.status) + '  ' + str(self.oborot) +
                          '\n      Порядковый номер алерта ' + str(u'\U00002796' + ' ') + str(self.alert_number) +
                          '\n      сейчас в работе за ' + str(u'\U00002796' + ' ') + str(
                            self.who_took) + '\n      сервер упал в ' + str(u'\U00002796' + ' ') +
                          str(self.when_down_present) + '\n      Алерты сервера активированы ' +
                          str(u'\U00002796' + ' ') + str(self.active) + '\n      Важность сервера ' + str(self.rare))
        else:
            status = (' Имя сервера ' + str(u'\U00002796' + ' ') + str(self.name) +
                      '\n      Cтатус сервера '
                      + str(u'\U00002796' + ' ') + str(self.status) + '  ' + str(self.oborot) +
                      '\n      Алерты сервера активированы ' + str(u'\U00002796' + ' ') +
                      str(self.active) + '\n      Важность сервера ' + str(self.rare))

        return status

    def show_name_whotook(self):
        info = (' Сервер: ' + str(self.name) + str(' ' + u'\U0001F6E0' + ' ') + 'Кто работает: ' + str(self.who_took))
        return info


class Person:
    def __init__(self, name, short_number, long_number, telegram_name, priory, telegram_id, is_dejurniy):
        self.name = name
        self.short_number = short_number
        self.long_number = long_number
        self.telegram_name = telegram_name
        self.priory = priory
        self.telegram_id = telegram_id
        self.is_dejurniy = is_dejurniy

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return format(self.name + ' ' + self.telegram_name)

    def show_person(self):
        person_info = str(f"{self.name}\n"
                          f"\U0001F4DE Короткий номер: {self.short_number}\n"
                          f"\U0001F4F1 Мобильный номер: {self.long_number}\n"
                          f"\U00002709 Телеграм: <a href='https://t.me/{self.telegram_name}'>"
                          f"{self.telegram_name}</a>\n")
        return person_info


"""создание объекта из класса для теста"""
# test = Server_data('test', 'raz')
# test.show_server_status()

# return '{}({!r})'.format(self.__class__.__name__, self.status)
"""************************************"""
