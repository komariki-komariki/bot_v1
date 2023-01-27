from yl import zakl
import os

def interface():
    a = input('1 - заключение по работодателю\n'
              '2 - заключение по контрагенту\n'
              '3 - заключение по ТСП\n'
              '4 - заключение по счету\n\n'
              'Введите код необходимого заключения: ')
    if a == '1':
        type_zakl = 'employer'
    if a == '2':
        type_zakl = 'counter'
    if a == '3':
        type_zakl = 'ekv'
    if a == '4':
        type_zakl = 'score'
    else:
        print('Введите корректный код')
    inn = input('Введите ИНН юридического лица: ')

    zapros = {
        'inn': inn,
        'type': type_zakl,
    }
    zakl(zapros['inn'], zapros['type'], 'komaroff.ilya.s@gmail.com')
    # os.remove(f'data_{inn}.json')

interface()


