
"""  Парсит файл График_дежурства.xlsx и возвращает список словарей типа
 {'day_number': datetime.date(2022, 5, 4), 'phone_number': 581}   """
import pickle


def dejurnie():
    import pandas as pd
    import datetime

    excel_data = pd.read_excel('/projects/sb_bot/data/dej_graph.xlsx')
    pikperson = '/projects/sb_bot/data/pikperson.dat'
    data = pd.DataFrame(excel_data, )
    month_list = []
    y = 0
    y_new = 1
    c = 0
    srez_comp = data.iloc[0:25, 1:8].iloc[4, 0].split(' ')

    for n in range(1, 8):

        x = 0
        x_new = 4

        for i in range(1, 6):

            srez = data.iloc[0:20, 1:8]
            times_srez = srez.iloc[x:x_new, y:y_new]
            x = x_new
            my_date = times_srez.iloc[0, 0].split(' ')
            my_month = my_date[1]
            my_date = my_date[0]

            if my_month == srez_comp[1]:
                my_date_converted = datetime.date.today().replace(day=int(my_date))

                number_a = times_srez.iloc[2, 0]
                number_b = times_srez.iloc[3, 0]
                number = pd.Series([number_a, number_b], dtype='Int64').sum()

                month_list.append({})
                month_list[c]['day_number'] = my_date_converted
                month_list[c]['telegram_name'] = ''
                month_list[c]['short_number'] = number
                month_list[c]['long_number'] = 0
                month_list[c]['name'] = ''

                with open(pikperson, mode='rb') as f:
                    times = pickle.load(f)

                for k in times:
                    j = month_list[c]['short_number']
                    if k.short_number == j:
                        month_list[c]['name'] = k.name
                        month_list[c]['telegram_name'] = k.telegram_name
                        month_list[c]['long_number'] = k.long_number
                c = c + 1
            x_new = x_new + 4

        y = y_new
        y_new = y_new + 1

    month_list = sorted(month_list, key=lambda k: k['day_number'])

    print("SYSTEM: script dejurnie completed")
    return month_list


if __name__ == '__main__':
    print('hello world')
