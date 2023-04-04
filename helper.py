import json
from pprint import pprint

def okrug(my_int):
    if my_int <0:
        my_int = -my_int
    num_list = [1000, 1000000, 1000000000, 1000000000000]
    result_list = []
    if len(str(my_int)) < 10 and len(str(my_int)) >= 7:
        nam = 'млн'
    if len(str(my_int)) < 7 and len(str(my_int)) >= 4:
        nam = 'тыс.'
    if len(str(my_int)) < 13 and len(str(my_int)) >= 10:
        nam = 'млрд'
    if len(str(my_int)) < 16 and len(str(my_int)) >= 13:
        nam = 'трлн'
    if len(str(my_int)) < 4 or len(str(my_int)) >= 16:
        nam = ''
    for min_count in num_list:
        count = my_int/min_count
        if count >= 1:
            result_list.append(round(count, 1))
        else:
            result_list.append(my_int)
    return f'{str(min(result_list)).replace(".",",")} {nam}'


def razdel(my_int):
    result = '{0:,}'.format(my_int).replace(',',' ')
    return result


# print(razdel(15522335582244.05))
# with open('data_fin//data_7715430318.json', 'r') as f:
#   fin_data = json.load(f)
#   a = fin_data['data']['2021']['2400']
#   print(okrug(a))