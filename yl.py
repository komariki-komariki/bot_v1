import json
import locale
import os

from docxtpl import DocxTemplate
from datetime import datetime

from ofdata_api import zapros_ogrn, zapros
from fl_oop import physical
from sendmail import sendmail



locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"
)

found_dictonary = {}
founder_fl_list = []
today = datetime.now().strftime('%Y-%m-%d')

def str_date(my_str):
    mounths = {
        '01': 'января',
        '02': 'февраля',
        '03': 'марта',
        '04': 'апреля',
        '05': 'мая',
        '06': 'июня',
        '07': 'июля',
        '08': 'августа',
        '09': 'сентября',
        '10': 'октября',
        '11': 'ноября',
        '12': 'декабря',
    }
    split_date = my_str.split('-')
    str_d = f'"{split_date[2]}" {mounths[split_date[1]]} {split_date[0]}'
    return str_d

class Ul:
    def __init__(self, inn, ogrn, full_name, abbreviated_name,
                 date_reg, status, legal_adress, okved, reg_fns,
                 reg_pfr, reg_fss, authorized_capital, management_company,
                 manager, founders, register_of_shareholders, license,
                 divisions, legal_successor, legal_successor_2, contacts,
                 nalogs, rmsp, average_number, unscrupulous_supplier,
                 disqualified_persons, mass_manager, mass_founder, meta_info
                                                                              ):
        self.inn = inn #ИНН
        self.ogrn = ogrn #ОГРН
        self.full_name = full_name #Полное наименование
        self.abbreviated_name = abbreviated_name #Сокращенное наименование
        self.date_reg = date_reg #Дата регистрации
        self.status = status #Статус
        self.legal_adress = legal_adress #Юридический адрес
        self.okved = okved #Вид деятельности
        self.reg_fns = reg_fns #ИФНС
        self.reg_pfr = reg_pfr #ПФР
        self.reg_fss = reg_fss #ФСС
        self.authorized_capital = authorized_capital #Уставный капитал
        self.management_company = management_company #Управляющая компания
        self.manager = manager #Директор
        self.founders = founders #Учредители
        self.register_of_shareholders = register_of_shareholders #Реест АО
        self.license = license #Лицензии
        self.divisions = divisions #Филиалы
        self.legal_successor = legal_successor #Правопредшественники
        self.legal_successor_2 = legal_successor_2 #Правопреемники
        self.contacts = contacts #Контакты
        self.nalogs = nalogs #Налоги
        self.rmsp = rmsp #РСМП
        self.average_number = average_number #Среднесписочная численность
        self.unscrupulous_supplier = unscrupulous_supplier #Недобросовестный поставщик
        self.disqualified_persons = disqualified_persons #Дисквалифицированные лица
        self.mass_manager = mass_manager #Массовый руководитель
        self.mass_founder = mass_founder #Массовый учредитель
        self.meta_info = meta_info #Мета

    def average(self):
        average_dict = []
        if self.average_number is None:
            average_dict.append('Сведения отсутствуют')
        else:
            average_dict.append(f'Среднесписочная численность, согласно данным ФНС - {self.average_number} человек')
        return average_dict

    def registry_holder(self):
        reg_holder = []
        if len(self.register_of_shareholders) > 0:
            reg_holder.append(
                    f"Держатель реестра акционеров - "
                    f"{self.register_of_shareholders['НаимПолн']} "
                    f"(ОГРН: {self.register_of_shareholders['ОГРН']})")
        else:
            reg_holder.append('')
        return reg_holder


    def manager_data(self):
        mng_list = []
        for manager_data in self.manager:
            if 'ОгрДоступ' in manager_data:
                restricted_access = manager_data['ОгрДоступ']
                if restricted_access == True:
                    mng_list.append('Доступ к сведениям ограничен (ФЗ от '
                                    '08.08.2001 г. №129-ФЗ "О государственной '
                                    'регистрации юридических лиц и индивидуальных'
                                    ' предпринимателей"')
            else:
                post_mng = manager_data['НаимДолжн'].capitalize()
                name_mng = manager_data['ФИО']
                inn_mng = manager_data['ИНН']
                unreliability_mng = manager_data['Недост']
                sv_ruk_mng = manager_data['СвязРуковод']
                sv_uchr_mng = manager_data['СвязУчред']
                diskv_mng = manager_data['ДисквЛицо']
                mass_mng = manager_data['МассРуковод']
                un_uch_mng = list(set(sv_uchr_mng + sv_ruk_mng))
                mng_list.append(f'{post_mng} {name_mng}, ИНН {inn_mng}')
        return mng_list

    def sole_executive_body(self):
        if len(self.management_company) > 0:
            return f'Управляющая компания {self.management_company["НаимПолн"]},' \
                   f' ИНН {self.management_company["ИНН"]}'
        if len(self.manager) > 0:
            return self.manager_data()

    def founderss(self):
        founders_list = []
        if len(self.founders['ФЛ']) > 0:
            founders_list.append("".join(self.founder_fl()))
        if len(self.founders['РосОрг']) > 0:
            founders_list.append("".join(self.founder_ul()))
        if len(self.founders['РФ']) > 0:
            founders_list.append("".join(self.founder_rf()))
        if len(self.founders['ПИФ']) > 0:
            founders_list.append("".join(self.founder_pif()))
        if len(self.founders['ИнОрг']) > 0:
            founders_list.append("".join(self.founder_ul_in()))
        if len(founders_list) == 0:
            founders_list.append('Сведения об учредителях отсутствуют')
        return founders_list

    def founder_ul(self):
        founders_list = []
        for founder in self.founders['РосОрг']:  # Учредитель ЮЛ
            if 'ОгрДоступ' in founder:
                restricted_access = founder['ОгрДоступ']
                if restricted_access == True:
                    founders_list.append('Доступ к сведениям ограничен (ФЗ от '
                                    '08.08.2001 г. №129-ФЗ "О государственной '
                                    'регистрации юридических лиц и индивидуальных'
                                    ' предпринимателей"')
            else:
                name_founder = founder['НаимПолн']
                ogrn_founder = founder['ОГРН']
                inn_founder = founder['ИНН']
                fraction_money = founder['Доля']['Номинал']
                fraction_percent = founder['Доля']['Процент']
                founders_list.append(f'\n- {name_founder}, ИНН {inn_founder} - ' \
                       f'{fraction_percent}% в УК ({fraction_money} рублей);')
        return founders_list

    def founder_ul_in(self):
        founders_list = []
        for founder_foreigner in self.founders['ИнОрг']:  # Учредитель нерезидент
            if 'ОгрДоступ' in founder_foreigner:
                restricted_access = founder_foreigner['ОгрДоступ']
                if restricted_access == True:
                    founders_list.append('Доступ к сведениям ограничен (ФЗ от '
                                    '08.08.2001 г. №129-ФЗ "О государственной '
                                    'регистрации юридических лиц и индивидуальных'
                                    ' предпринимателей"')
            else:
                name_founder = founder_foreigner['НаимПолн']
                grn_founder = founder_foreigner['РегНомер']
                fraction_money = founder_foreigner['Доля']['Номинал']
                fraction_percent = founder_foreigner['Доля']['Процент']
                country = founder_foreigner['Страна']
                founders_list.append(
                    f'\n- {name_founder}, рег.№ {grn_founder}, '
                    f'{country} - {fraction_percent}% в '
                    f'УК ({fraction_money} рублей);\n')
        return founders_list

    def founder_rf(self):
        return list('Учредителем является РФ. Надо разбираться, такие компании еще не встречались')

    def founder_pif(self):
        return list('Учредителем является ПИФ. Надо разбираться, такие компании еще не встречались')

    def founder_fl(self):
        founders_list = []
        for founder in self.founders['ФЛ']:  # Учредитель ФЛ
            if 'ОгрДоступ' in founder:
                restricted_access = founder['ОгрДоступ']
                if restricted_access == True:
                    founders_list.append('Доступ к сведениям ограничен (ФЗ от '
                                         '08.08.2001 г. №129-ФЗ "О государственной '
                                         'регистрации юридических лиц и индивидуальных'
                                         ' предпринимателей"')
            else:
                fio_founder = founder['ФИО']
                inn_founder = founder['ИНН']
                fraction_money = founder['Доля']['Номинал']
                fraction_percent = founder['Доля']['Процент']
                communication_by_supervisor = founder['СвязРуковод']
                communication_by_founder = founder['СвязУчред']
                un_uch_mng = list(set(communication_by_supervisor + communication_by_founder))
                founders_list.append(f'- {fio_founder}, {inn_founder} - {fraction_percent}% в УК ({fraction_money} рублей);\n')
                found_dictonary[inn_founder] = un_uch_mng
        return founders_list

    def negative(self):
        if self.unscrupulous_supplier == False:
            unscrupulous_supplier = 'Нет'
        else:
            unscrupulous_supplier = 'Да'
        if self.disqualified_persons == False:
            disqualified_persons = 'Нет'
        else:
            disqualified_persons = 'Да'
        if self.mass_manager == False:
            mass_manager = 'Нет'
        else:
            mass_manager = 'Да'
        if self.mass_founder == False:
            mass_founder = 'Нет'
        else:
            mass_founder = 'Да'
        result = f'Присутствие дисквалифицированных лиц в руководстве компании: {disqualified_persons}\n' \
                 f'Присутствие массовых руководителей: {mass_manager}\n' \
                 f'Присутствие массовых учредителей: {mass_founder}\n' \
                 f'Присутствие в перечне недобросовестных поставщиков: {unscrupulous_supplier}\n'
        return result

    def contactss(self):
        cont_list = []
        if len(self.contacts) > 0:
            for k, v in self.contacts.items():
                cont_list.append(f'{k}: {v}\n')
        else:
            cont_list.append('Контактные данные в ЕГРЮЛ отсутствуют')
        return cont_list

    def filialss(self):
        filials_list = []
        if 'Филиал' in self.divisions.keys():  # Филиалы
            for filial in self.divisions['Филиал']:
                fil_adress = filial['Адрес']
                fil_kpp = filial['КПП']
                fil_name = filial['НаимПолн']
                filials_list.append(
                    f'\n- {fil_name} (КПП: {fil_kpp})\nрасположен по адресу: {fil_adress}')
        if 'Представ' in self.divisions.keys():  # Представительства
            for preds in self.divisions['Представ']:
                preds_name = preds['НаимПолн']
                preds_country = preds['Страна']
                filials_list.append(
                    f'\n- Представительство "{preds_name}" (Страна: {preds_country})')
        else:
            filials_list.append(
                'Согласно сведениям ЕГРЮЛ организация не имеет филиалов')
        return filials_list

    def lic(self):
        permission_list = []
        if len(self.license) == 0:  # Лицензии
            permission_list.append(
                'В ЕГРЮЛ отсутствуют сведения о выданных лицензиях')
        else:
            for lic in self.license:
                deyat = lic['ВидДеят']
                date = datetime.strptime(lic['Дата'], '%Y-%m-%d')
                org = lic['ЛицОрг']
                numb = lic['Номер']
                permission_list.append(
                    f'\n- Лицензия № {numb} от {date.date().strftime("%d.%m.%Y")}'
                    f' г.;\nВыдавший орган: {org.upper()};'
                    f'\nРазрешенные виды деятельности: {"; ".join(deyat)}')
        return permission_list

    def union_foo(self):
        director = self.sole_executive_body()
        founders = self.founderss()
        contacts = self.contactss()
        negative = self.negative()
        reg_holder = self.registry_holder()
        for k, v in found_dictonary.items():
            if len(v) > 0:
                founder_fl_list.append(k)
        summary_dictionary = {'inn': self.inn,
                              'ogrn': self.ogrn,
                              'full_name': self.full_name,
                              'abr_name': self.abbreviated_name,
                              'legal_adress': self.legal_adress['АдресРФ'],
                              'authorized_capital': f'{self.authorized_capital["Тип"].capitalize()} '
                                                    f'{self.authorized_capital["Сумма"]} рублей',
                              'manager': "".join(director),
                              'founders': "".join(founders),
                              'date_reg': str_date(self.date_reg).replace('"', ''),
                              'chisl': "".join(self.average()),
                              'okved': f'{self.okved["Наим"]} (код ОКВЭД: {self.okved["Код"]})',
                              'contacts': contacts,
                              'negative': negative,
                              'filials': "\n".join(self.filialss()),
                              'licensse': "\n".join(self.lic()),
                              'reg_holder': "".join(reg_holder),
                              'ifns': self.reg_fns['НаимОрг'],
                              'status': self.status['Наим'],
                              'today': str_date(today),

        }
        return summary_dictionary

def instance(json_file):
    with open(json_file, 'r') as f:
        json_file = json.load(f)
    orgs = Ul(
        json_file['data']['ИНН'],
        json_file['data']['ОГРН'],
        json_file['data']['НаимПолн'],
        json_file['data']['НаимСокр'],
        json_file['data']['ДатаРег'],
        json_file['data']['Статус'],
        json_file['data']['ЮрАдрес'],
        json_file['data']['ОКВЭД'],
        json_file['data']['РегФНС'],
        json_file['data']['РегПФР'],
        json_file['data']['РегФСС'],
        json_file['data']['УстКап'],
        json_file['data']['УпрОрг'],
        json_file['data']['Руковод'],
        json_file['data']['Учред'],
        json_file['data']['ДержРеестрАО'],
        json_file['data']['Лиценз'],
        json_file['data']['Подразд'],
        json_file['data']['Правопредш'],
        json_file['data']['Правопреем'],
        json_file['data']['Контакты'],
        json_file['data']['Налоги'],
        json_file['data']['РМСП'],
        json_file['data']['СЧР'],
        json_file['data']['НедобПост'],
        json_file['data']['ДисквЛица'],
        json_file['data']['МассРуковод'],
        json_file['data']['МассУчред'],
        json_file['meta'])
    return orgs

def info_uch_mng(my_list): #проверка наличия файла
    for ogrn in my_list:
        if not f'data_{ogrn}.json' in os.listdir('data_emp'):
            zapros_ogrn(ogrn)

def word_foo(my_dict, type_zakl):
    doc = DocxTemplate(f"patterns//{type_zakl}.docx")
    context = my_dict
    doc.render (context)
    short_name = my_dict["abr_name"].replace('"', "").replace("\\", '')
    date = datetime.now().date().strftime('%d.%m.%Y')
    file_name = f"{type_zakl}_{short_name}_{date}.docx"
    doc.save(file_name)
    return file_name

def remove_data(str_dir):
    if len(os.listdir(str_dir)) > 0:
        for file_names in os.listdir(str_dir):
            os.remove(f'{str_dir}/{file_names}')

def zakl(inn, type_zakl,adress): #Принимает 3 строки: инн и тип заключения (counter - контрагент; ekv - эквайринг, score - счет, employer - работодатель) и адрес эл. почты.
    zapros(inn)
    try:
        orgs = instance(f'data_json_files//data_{inn}.json')
        osn = orgs.union_foo()
        if type_zakl == 'employer':
            word_foo(orgs.union_foo(), type_zakl)
        if type_zakl == 'score' or 'counter' or 'ekv':
            if len(founder_fl_list) > 0:
                fl = physical(founder_fl_list)
            else:
                fl = {
                    'uchastie': 'Учредители организации в иных действующих юридических'
                                ' лицах участия не принимают'
                }
            svod = osn | fl
            sendmail(word_foo(svod, type_zakl), adress)
            remove_data('data_json_files')
            remove_data('data_emp')
            remove_data('data_fl')
            return 'Успешно'
    except: return 'Сбой'




