import json
import requests
from tokens import token_ofdata
from pprint import pprint
from yl import Ul, instance
from ofdata_api import zapros
from datetime import datetime, timedelta

# def zapros_law(inn):
#     inn = inn
#     url = f'https://api.ofdata.ru/v2/legal-cases?key={token_ofdata}&inn={inn}&role=defendant&sort=-date'
#     response = requests.get(url).json()
#     count = 100 - response['meta']['today_request_count']
#     # Count.ost = f'осталось запросов: {str(count)}'
#     # with open('logs/logs.txt', "a", encoding='UTF8') as log:
#     #     log.write(f"Запрос ЮЛ по ИНН: {inn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
#     with open(f'data_law//data_law_{inn}.json', 'w') as f:
#         json.dump(response, f)
#     return response


# def zapros_pr(inn):
#     inn = inn
#     url = f'https://api.ofdata.ru/v2/inspections?key={token_ofdata}&inn={inn}&sort=-date'
#     response = requests.get(url).json()
#     count = 100 - response['meta']['today_request_count']
#     # Count.ost = f'осталось запросов: {str(count)}'
#     # with open('logs/logs.txt', "a", encoding='UTF8') as log:
#     #     log.write(f"Запрос ЮЛ по ИНН: {inn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
#     with open(f'data_pr//data_pr_{inn}.json', 'w') as f:
#         json.dump(response, f)
#     return response


# zapros_pr('7702070139')

# zapros('5003046732')

with open('data_fin//data_9706016908.json', 'r') as f:
    json_file = json.load(f)
    # pprint(json_file['data'])
    # for x in json_file['data']['Записи']:
    #     if x['Наруш'] is True:
    #         print(f'- {x["ТипРасп"]} ({x["ТипПров"].lower()}) №{x["Номер"]}.\n'
    #                   f'Дата начала: {x["ДатаНач"]}; дата окончания: {x["ДатаОконч"]}.\n'
    #                   f'Цель: {x["Цель"]}.\nКонтролирующий орган: {x["ОргКонтр"]["Наим"]}.\n'
    #               f'Нарушение: {x["Объекты"]}')
    #
    pprint(json_file)
    # for x in json_file['data']['Записи']:
    #     print(x)
        # if x['Заверш'] is False:
        #     print(x)


# a = instance('data_json_files//data_7707818812.json')
# # print(a.founder_ul_in())
# pprint(a.founder_ul_in())
#
# list_enemy = ['АВСТРАЛИЯ',
#              'АЛБАНИЯ',
#              'АНДОРРА',
#              'ВЕЛИКОБРИТАНИЯ',
#              'АВСТРИЯ',
#              'БЕЛЬГИЯ',
#              'БОЛГАРИЯ',
#              'ВЕНГРИЯ',
#              'ГЕРМАНИЯ',
#              'ИРЛАНДИЯ',
#              'ИСПНИЯ',
#              'ИТАЛИЯ',
#              'КИПР',
#              'ЛАТВИЯ',
#              'ЛИТВА',
#              'ЛЮКСЕМБУРГ',
#              'НИДЕРЛАНДЫ',
#              'ПОЛЬША',
#              'ПОРТУГАЛИЯ',
#              'РУМЫНИЯ',
#              'ФИНЛЯНДИЯ',
#              'ФРАНЦИЯ',
#              'ЧЕХИЯ',
#              'ШВЕЦИЯ',
#              'ЭСТОНИЯ',
#              'ИСЛАНДИЯ',
#              'КАНАДА',
#              'ЛИХТЕНШТЕЙН',
#              'МИКРОНЕЗИЯ',
#              'МОНАКО',
#              'НОВАЯ ЗЕЛАНДИЯ',
#              'НОРВЕГИЯ',
#              'ЮЖНАЯ КОРЕЯ',
#              'САН-МАРИНО',
#              'СЕВЕРНАЯ МАКЕДОНИЯ',
#              'СИНГАПУР',
#              'США',
#              'ТАЙВАНЬ',
#              'УКРАИНА',
#              'ЧЕРНОГОРИЯ',
#              'ШВЕЙЦАРИЯ',
#              'ЯПОНИЯ', 'БАГАМЫ', 'ГРЕЦИЯ', 'ДАНИЯ', 'МАЛЬТА', 'СЛОВАКИЯ', 'СЛОВЕНИЯ', 'ХОРВАТИЯ'
#              ]
#
# # print(sorted(list_enemy))
# # print(len(list_enemy))
# # for founder_foreigner in a.founders['ИнОрг']:
# #     name_founder = founder_foreigner['НаимПолн']
# #     grn_founder = founder_foreigner['РегНомер']
# #     fraction_money = founder_foreigner['Доля']['Номинал']
# #     fraction_percent = founder_foreigner['Доля']['Процент']
# #     country = founder_foreigner['Страна']
# #     if country.upper() in list_enemy:
# #         print(f'Учредитель - юридическое лицо, '
# #               f'зарегистрированное в соответствием законодательством '
# #               f'недружественного государства ({country}).')
#
