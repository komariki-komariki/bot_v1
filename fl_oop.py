import json
import os

from ofdata_api import zapros_fl



class Fl:
    def __init__(self, inn, name, mass_mng, mass_founder, unscrupulous_supplier, businessman, mng, founder ):
        self.inn = inn #ИНН
        self.name = name #ФИО
        self.mass_mng = mass_mng #Массовый руководитель
        self.mass_founder = mass_founder #Массовыйй учредитель
        self.unscrupulous_supplier = unscrupulous_supplier  # НедобПост
        self.businessman = businessman #ИП
        self.mng = mng #Руководитель
        self.founder = founder #Учредитель

    def participation(self):
        my_list = []
        if len(self.founder) > 0:
            for i in self.founder:
                if i['Статус'] == 'Действует':
                    ogrn = i['ОГРН']
                    inn = i['ИНН']
                    name = i['НаимПолн']
                    date_reg = i['ДатаРег']
                    legal_adress = i['ЮрАдрес']
                    okved = i['ОКВЭД']
                    my_list.append(f'\n{name}\nИНН: {inn} ОГРН: {ogrn}\nДата регистрации:{date_reg}\nВид деятельности: {okved}\nЮридический адрес: {legal_adress}')
        if len(self.mng) > 0:
            for x in self.mng:
                if x['Статус'] == 'Действует':
                    ogrn = x['ОГРН']
                    inn = x['ИНН']
                    name = x['НаимПолн']
                    date_reg = x['ДатаРег']
                    legal_adress = x['ЮрАдрес']
                    okved = x['ОКВЭД']
                    my_list.append(
                        f'\n{name}\nИНН: {inn} ОГРН: {ogrn}\nДата регистрации:'
                        f'{date_reg}\nВид деятельности: {okved}\n'
                        f'Юридический адрес: {legal_adress}'
                    )
        if len(self.businessman) > 0:
            for y in self.businessman:
                if y['Статус'] == 'Действующий':
                    ogrn = y['ОГРНИП']
                    inn = y['ИНН']
                    date_reg = y['ДатаРег']
                    okved = y['ОКВЭД']
                    types = y['Тип']
                    name = y['ФИО']
                    my_list.append(
                    f'\n{types} {name}\nИНН: {inn} ОГРНИП: {ogrn}\nДата регистрации:'
                    f'{date_reg}\nВид деятельности: {okved}\n')
        if  len(my_list) == 0:
            my_list.append(
                f'\n{name} в действующих юридических лицах участие не '
                f'принимает, в качестве индивидуального предпринимателя не зарегистрирован(а)')
        return my_list

    def info_fl(self):
        my_list = []
        my_list.append(f'\n{self.name} принимает участие в следующих организациях: {"".join(self.participation())}')
        return my_list


def instance_fl(json_file):
    with open(json_file, 'r') as f:
        json_file = json.load(f)
    person = Fl(
        json_file['data']['ИНН'],
        json_file['data']['ФИО'],
        json_file['data']['МассРуковод'],
        json_file['data']['МассУчред'],
        json_file['data']['НедобПост'],
        json_file['data']['ИП'],
        json_file['data']['Руковод'],
        json_file['data']['Учред'],
    )
    return person

def physical(my_list):
    sv = []
    for inn_fl in my_list:
        if not f'data_{inn_fl}.json' in os.listdir('data_fl'):
            zapros_fl(inn_fl)
        fl_data = instance_fl(f'data_fl//data_{inn_fl}.json')
        sv.append("".join(fl_data.info_fl()))
    return {'uchastie': "\n".join(sv)}


