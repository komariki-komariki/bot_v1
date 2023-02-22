import json
from pprint import pprint
from yl import Ul, instance
from ofdata_api import zapros
from datetime import datetime, timedelta

from who import domain_data

# zapros('9731093039')
# with open('data_json_files/data_7717790355.json', 'r') as f:
#     json_file = json.load(f)
#     pprint(json_file)

a = instance('data_json_files/data_7801595578.json')
# print(a.contacts)
# if len(a.contacts) > 0:

# def contactss():
#     cont_list = []
#     try:
#         if len(a.contacts) > 0:
#             cont_dict = {'Телефоны': "; ".join(a.contacts['Тел']), 'E-mail': "; ".join(a.contacts['Емэйл']), 'Сайт': a.contacts['ВебСайт'],}
#             if cont_dict['Сайт'] is not None:
#                 domain_info = domain_data(cont_dict['Сайт'])
#         else:
#             print(('Контактные данные в ЕГРЮЛ отсутствуют'))
#         #     cont_list.append('Контактные данные в ЕГРЮЛ отсутствуют')
#     except Exception as e:
#         cont_list.append(f'ОШИБКА: {str(e)}')
#     return cont_dict
#
def site():
    if len(a.contacts) > 0:
        if a.contacts['ВебСайт'] is None:
            data_site = 'Нет данных'
        else:
            domain_info = domain_data(a.contacts['ВебСайт'])
            data_site =  f'{a.contacts["ВебСайт"]}\n{"".join(domain_info)}'
    return data_site


def phone():
    try:
        if len(a.contacts) > 0:
            if len(a.contacts['Тел']) > 0:
                phones = "; ".join(a.contacts['Тел'])
            else:
                phones = 'Нет данных'
        else:
            phones = 'Нет данных'
        return phones
    except Exception as e:
        return f'ОШИБКА: {str(e)}'



def el_post():
    try:
        if len(a.contacts) > 0:
            if len(a.contacts['Емэйл']) > 0:
                mails = "; ".join(a.contacts['Емэйл'])
            else:
                mails = 'Нет данных'
        else:
            mails = 'Нет данных'
        return mails
    except Exception as e:
        return f'ОШИБКА: {str(e)}'
#

# def days_reg():
#     try:
#         date = datetime.now()
#         date_2 = datetime.strptime(a.date_reg, '%Y-%m-%d')
#         days = date - date_2
#         delta = timedelta(days = 547,
#                           seconds = 0,
#                           microseconds = 0,
#                           milliseconds = 0,
#                           minutes = 0,
#                           hours = 0,
#                           weeks = 0)
#         if days > delta:
#             return f'{days.days} дней (БОЛЕЕ 1,5 ЛЕТ)'
#         else:
#             return f'{days.days} дней (МЕНЕЕ 1,5 ЛЕТ)'
#     except Exception as e:
#         return f'ОШИБКА: {str(e)}'

# print(el_post())