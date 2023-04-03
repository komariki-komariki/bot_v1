import json
from fl_oop import physical
from datetime import datetime

from yl import str_date,today, word_foo, remove_data
from ofdata_api import zapros_ip
from sendmail import sendmail
from proverki import pages


# with open('data_ip/data_501206285115.json', 'r', encoding='UTF8') as f:
#     json_file = json.load(f)
#     pprint(json_file)


def abr_name_fl(my_str):
    name_list = my_str.split()
    if len(name_list) == 3:
        format_name = '{} {}.{}.'.format(name_list[0], name_list[1][0], name_list[2][0])
        return format_name
    else:
        return my_str

class Ip:
    def __init__(self, date_reg, inn, ogrnip, okato, okved, rmsp,
                 ifns, status, types, abr_types, name, lic, mass_manager,
                 mass_founder, unscrupulous_supplier, communication_by_founder,
                 communication_by_mng,
                 ):
        self.date_reg = date_reg
        self.inn = inn
        self.ogrnip = ogrnip
        self.okato = okato
        self.okved = okved
        self.rmsp = rmsp
        self.ifns = ifns
        self.status = status
        self.types = types
        self.abr_types = abr_types
        self.name = name
        self.lic = lic
        self.mass_manager = mass_manager
        self.mass_founder = mass_founder
        self.unscrupulous_supplier = unscrupulous_supplier
        self.communication_by_founder = communication_by_founder
        self.communication_by_mng = communication_by_mng

    def rsmp(self):
        rmsp_list = []
        date = datetime.strptime(self.rmsp["ДатаВкл"], '%Y-%m-%d')
        try:
            if len(self.rmsp) > 0:
                rmsp_list.append(
                    f'Имеется информация о включении {self.abr_types} {abr_name_fl(self.name)} в '
                    f'Единый реестр субъектов малого и среднего '
                    f'предпринимательства:\nТип: {self.rmsp["Кат"].capitalize()}; '
                    f'Дата включения: {date.date().strftime("%d.%m.%Y")} г.')
            else:
                rmsp_list.append(
                    f'Сведения о включении {self.abr_types} {abr_name_fl(self.name)} в '
                    f'Единый реестр субъектов малого и среднего '
                    f'предпринимательства отсутствуют')

        except Exception as e:
            rmsp_list.append(f'ОШИБКА: {str(e)}')
        return rmsp_list

    def ip_fl(self):
        fl=[]
        try:
            if len(self.communication_by_founder) or len(
                    self.communication_by_mng) > 0:
                fl.append(self.inn)
                return physical(fl)
            else:
                return {'uchastie': 'Индивидуальный предприниматель в иных действующих юридических'
                                ' лицах участия не принимает'}
        except Exception as e:
            return {'uchastie': f'ОШИБКА: {str(e)}'}

    def lic_ip(self):
        permission_list = []
        try:
            if len(self.lic) == 0:  # Лицензии
                permission_list.append(
                    'В ЕГРЮЛ отсутствуют сведения о выданных лицензиях.')
            else:
                for lic in self.lic:
                    deyat = lic['ВидДеят']
                    date = datetime.strptime(lic['Дата'], '%Y-%m-%d')
                    org = lic['ЛицОрг']
                    numb = lic['Номер']
                    permission_list.append(
                        f'\n- Лицензия № {numb} от {date.date().strftime("%d.%m.%Y")}'
                        f' г.;\nВыдавший орган: {org.upper()};'
                        f'\nРазрешенные виды деятельности: {"; ".join(deyat)}.')
        except Exception as e:
            permission_list.append(f'ОШИБКА: {str(e)}')
        return permission_list

    def negative(self):
        try:
            if self.unscrupulous_supplier == False:
                unscrupulous_supplier = 'Нет'
            else:
                unscrupulous_supplier = 'Да'

            if self.mass_manager == False:
                mass_manager = 'Нет'
            else:
                mass_manager = 'Да'
            if self.mass_founder == False:
                mass_founder = 'Нет'
            else:
                mass_founder = 'Да'
            result = f'- Массовый руководитель: {mass_manager};\n' \
                     f'- Массовых учредитель: {mass_founder};\n' \
                     f'- Недобросовестный поставщик: {unscrupulous_supplier}.\n'

        except Exception as e:
            result = f'ОШИБКА: {str(e)}'
        return result

    def union_foo_ip(self):
        negative = self.negative()
        capital = 'Уставный капитал не предусмотрен организационно-правовой формой'
        summary_dictionary = {'inn': self.inn,
                              'ogrn': self.ogrnip,
                              'full_name': f'{self.types} {self.name}',
                              'abr_name': f'{self.abr_types} {abr_name_fl(self.name)}',
                              'legal_adress': 'СВЕДЕНИЯ ОТСУТСТВУЮТ',
                              'authorized_capital': capital,
                              'manager': f'{self.name}, ИНН {self.inn}',
                              'founders': f'{self.name}, ИНН {self.inn}',
                              'date_reg': str_date(self.date_reg).replace('"',
                                                                          ''),
                              'chisl': 'Сведения отсутствуют',
                              'okved': f'{self.okved["Наим"]} (код ОКВЭД: {self.okved["Код"]})',
                              'contacts': 'Сведения отсутствуют',
                              'negative': negative,
                              'filials': 'Не имеет филиалов',
                              'licensse': "\n".join(self.lic_ip()),
                              'reg_holder': "",
                              'ifns': self.ifns['НаимОрг'],
                              'status': self.status['Наим'],
                              'today': str_date(today),
                              'fssp': 'Автоматический запрос невозможен',
                              'rsmp': "".join(self.rsmp()),
                              'today_count': datetime.now().strftime("%d.%m.%Y")

                              }
        return summary_dictionary

def instance_ip(json_file):
    with open(json_file, 'r') as f:
        json_file = json.load(f)
    person = Ip(
        json_file['data']['ДатаРег'],
        json_file['data']['ИНН'],
        json_file['data']['ОГРНИП'],
        json_file['data']['ОКАТО'],
        json_file['data']['ОКВЭД'],
        json_file['data']['РМСП'],
        json_file['data']['РегФНС'],
        json_file['data']['Статус'],
        json_file['data']['Тип'],
        json_file['data']['ТипСокр'],
        json_file['data']['ФИО'],
        json_file['data']['Лиценз'],
        json_file['data']['МассРуковод'],
        json_file['data']['МассУчред'],
        json_file['data']['НедобПост'],
        json_file['data']['СвязУчред'],
        json_file['data']['СвязРуковод'],

    )
    return person

def zakl_ip(inn, type_zakl,adress): #Принимает 3 строки: инн и тип заключения (counter - контрагент; ekv - эквайринг, score - счет, employer - работодатель) и адрес эл. почты.
    try:
        zapros_ip(inn)
        prov = pages(inn)
        ip = instance_ip(f'data_ip//data_{inn}.json')
        osn = ip.union_foo_ip()
        if type_zakl == 'employer':
            word_foo(ip.union_foo_ip(), type_zakl)
        if type_zakl == 'score' or 'counter' or 'ekv':
            fl = ip.ip_fl()
            svod = osn | fl | prov
            sendmail(word_foo(svod, type_zakl), adress)
            remove_data('data_ip')
            remove_data('data_emp')
            remove_data('data_fl')
        return 'Успешно'
    except Exception as e:
        return f'ОШИБКА: {str(e)}'



# zakl_ip('522512439672', 'employer', 'komaroff.ilya.s@gmail.com')