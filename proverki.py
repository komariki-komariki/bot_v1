import json
import os
from ofdata_api import zapros_pr
from datetime import datetime, timedelta


def pages(inn):
    try:
        bez_narush = 0
        narush = 0
        itog = []
        sved_list = []
        date_now = datetime.now()
        zapros_pr(inn)
        for page in os.listdir('data_pr'):
            with open(f'data_pr//{page}', 'r') as f:
                json_file = json.load(f)
                if json_file['data']['ЗапВсего'] != 0:
                    for x in json_file['data']['Записи']:
                        if x['Наруш'] is True:
                            narush += 1
                            type_pr = f'{x["ТипРасп"]} ({x["ТипПров"]})'
                            num_pr = x["Номер"]
                            start_date = datetime.strptime(x["ДатаНач"], '%Y-%m-%d')
                            if x["ДатаОконч"] is None:
                                end_date = 'cведения отсутствуют'
                            else:
                                end_date = datetime.strptime(x["ДатаОконч"],
                                                             '%Y-%m-%d').date().strftime(
                                    "%d.%m.%Y")
                            purpose = x["Цель"]
                            control_body = x["ОргКонтр"]["Наим"]
                            violation = x["Объекты"]
                            for i in violation:
                                if len(i['Результ']) != 0:
                                    for q in i['Результ']['Наруш']:
                                        sut = q['Текст']
                                        for n in q['Предпис']:
                                            predpis = n['Текст']
                                            date_predpis = n['Дата']
                                            # date_predpis = datetime.strptime(n['Дата'], '%Y-%m-%d')
                                            days = date_now - start_date
                                            # print(days)
                                            delta = timedelta(days=730,
                                                              seconds=0,
                                                              microseconds=0,
                                                              milliseconds=0,
                                                              minutes=0,
                                                              hours=0,
                                                              weeks=0)
                                            if days < delta:
                                                sved_narush = f'\n- №{num_pr}.\nТип: {type_pr}\n' \
                                                              f'Орган контроля: {control_body}.' \
                                                              f'\nДата начала: {start_date.date().strftime("%d.%m.%Y")}; ' \
                                                              f'Дата окончания: {end_date}.\nЦель: {purpose}.\n' \
                                                              f'Суть нарушения: {sut}.\n' \
                                                              f'Предписание: {predpis}.\n' \
                                                              f'Срок выполнения: {date_predpis}.\n'
                                                sved_list.append(sved_narush)


                        if x['Наруш'] is False:
                            bez_narush += 1
                else:
                    sved_list.append(
                        'Сведения о проверках отсутствуют.')
        if len(sved_list) == 0:
            sved_list.append('Сведения о нарушениях за последние 730 дней не выявлены.')
        vsego = f"Всего найдено в ФГИС ЕРП: {json_file['data']['ЗапВсего']}\n" \
                f"С нарушениями: {narush}\n" \
                f"Подробно о проверках с нарушениями за последние 2 года:\n"
        itog.append(vsego)
        pr_dict = {'proverki': "".join(itog + sved_list)}
        if len(os.listdir('data_pr')) > 0:
            for file_names in os.listdir('data_pr'):
                os.remove(f'data_pr//{file_names}')
        return pr_dict
    except Exception as e:
        return {'proverki': f'ОШИБКА: {str(e)}'}

# zapros_pr('7710630056')
# from pprint import pprint
# with open(f'data_pr//data_pr_7727197296_page_1.json', 'r') as f:
#     json_file = json.load(f)
#     if json_file['data']['ЗапВсего'] != 0:
#         pass
#     else:
#         print('not found')
#
# print(pages('7710630056'))