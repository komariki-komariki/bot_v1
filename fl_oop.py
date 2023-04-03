import json
import os
from pprint import pprint
from datetime import datetime
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
        inn_list = []
        try:
            if len(self.founder) > 0:
                for i in self.founder:
                    if i['Статус'] == 'Не действует':
                        pass
                    else:
                        ogrn = i['ОГРН']
                        inn = i['ИНН']
                        name = i['НаимПолн']
                        date_reg = datetime.strptime(i['ДатаРег'], '%Y-%m-%d')
                        legal_adress = i['ЮрАдрес']
                        okved = i['ОКВЭД']
                        status = i['Статус']
                        inn_list.append(inn)
                        my_list.append(
                            f'\n{name}\nИНН: {inn} ОГРН: {ogrn}\nДата регистрации: '
                            f'{date_reg.date().strftime("%d.%m.%Y")} г.\nВид деятельности: {okved}\n'
                            f'Юридический адрес: {legal_adress}\nСтатус: {status}')
            if len(self.mng) > 0:
                for x in self.mng:
                    if x['Статус'] == 'Не действует':
                        pass
                    else:
                        ogrn_mng = x['ОГРН']
                        inn_mng = x['ИНН']
                        name_mng = x['НаимПолн']
                        date_reg_mng = datetime.strptime(x['ДатаРег'], '%Y-%m-%d')
                        legal_adress_mng = x['ЮрАдрес']
                        okved_mng = x['ОКВЭД']
                        status_mng = x['Статус']
                        if inn_mng in inn_list:
                            pass
                        else:
                            my_list.append(
                                f'\n{name_mng}\nИНН: {inn_mng} ОГРН: {ogrn_mng}\nДата регистрации: '
                                f'{date_reg_mng.date().strftime("%d.%m.%Y")} г.\nВид деятельности: {okved_mng}\n'
                                f'Юридический адрес: {legal_adress_mng}\nСтатус: {status_mng}'
                            )
            if len(self.businessman) > 0:
                for y in self.businessman:
                    if y['Статус'] == 'Недействующий':
                        pass
                    else:
                        ogrn_ip = y['ОГРНИП']
                        inn_ip = y['ИНН']
                        date_reg_ip = datetime.strptime(y['ДатаРег'], '%Y-%m-%d')
                        okved_ip = y['ОКВЭД']
                        types_ip = y['Тип']
                        name_ip = y['ФИО']
                        status_ip = y['Статус']
                        my_list.append(
                        f'\n{types_ip} {name_ip}\nИНН: {inn_ip} ОГРНИП: {ogrn_ip}\nДата регистрации: '
                        f'{date_reg_ip.date().strftime("%d.%m.%Y")} г.\nВид деятельности: {okved_ip}\nСтатус: {status_ip}')
            if  len(my_list) == 0:
                my_list.append(
                    f'\n{name} в действующих юридических лицах участие не '
                    f'принимает, в качестве индивидуального предпринимателя не зарегистрирован(а)')
            inn_list.clear()
        except Exception as e:
            my_list.append(f'ОШИБКА: {str(e)}')
        return my_list

    def info_fl(self):
        my_list = []
        try:
            my_list.append(f'\n{self.name} принимает участие в следующих организациях: {"".join(self.participation())}')
        except Exception as e:
            my_list.append(f'ОШИБКА: {str(e)}')
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

# zapros_fl('773406813937')
# a = instance_fl('data_fl//data_773406813937.json')
# pprint(a.participation())
