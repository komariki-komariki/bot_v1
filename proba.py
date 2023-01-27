from ofdata_api import zapros
from yl import instance
from pprint import pprint

a = instance('data_json_files/data_1435149030.json')

# pprint(a.nalogs)

nalogs_list =[]
if len(a.nalogs) == 0:
    nalogs_list.append('Сведения отсутствуют')
else:
    if len(a.nalogs['ОсобРежим']) > 0:
        nalogs_list.append(f'Применяется {"".join(a.nalogs["ОсобРежим"])}')
    else:
        nalogs_list.append('Особый налоговый режим не применяется')
    if len(a.nalogs['СведУпл']) > 0:
        for x in a.nalogs['СведУпл']:
            nalogs_list.append(f'\n{x["Наим"]}: {x["Сумма"]} рублей')
        nalogs_list.append(f'\nВсего уплачено: {a.nalogs["СумУпл"]} рублей')
        if a.nalogs['СумНедоим'] is None:
            nalogs_list.append('\nСведения о недоимках отсутствуют')
        else:
            nalogs_list.append(a.nalogs['СумНедоим'])
print(nalogs_list)



