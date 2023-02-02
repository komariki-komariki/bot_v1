import json
import requests
import datetime

from tokens import token_ofdata

class Count():
    ost = ''
    def __init__(self):
        return

count = []

def zapros(inn):
    inn = inn
    url = f'https://api.ofdata.ru/v2/company?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    count = 100 - response['meta']['today_request_count']
    Count.ost = f'осталось запросов {str(count)}'
    with open('logs/logs.txt', "a", encoding='UTF8') as log:
        log.write(f"Запрос ЮЛ по ИНН: {inn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
    with open(f'data_json_files//data_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_ogrn(ogrn):
    ogrn = ogrn
    url = f'https://api.ofdata.ru/v2/company?key={token_ofdata}&ogrn={ogrn}'
    response = requests.get(url).json()
    count = 100 - response['meta']['today_request_count']
    Count.ost = f'осталось запросов {str(count)}'
    with open('logs/logs.txt', "a", encoding='UTF8') as log:
        log.write(f"Запрос ЮЛ по ОГРН: {ogrn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
    with open(f'data_emp//data_{ogrn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_fl(inn):
    url = f'https://api.ofdata.ru/v2/person?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    count = 100 - response['meta']['today_request_count']
    Count.ost = f'осталось запросов {str(count)}'
    with open('logs/logs.txt', "a", encoding='UTF8') as log:
        log.write(f"Запрос ФЛ по ИНН: {inn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
    with open(f'data_fl//data_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_ip(inn):
    url = f'https://api.ofdata.ru/v2/entrepreneur?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    count = 100 - response['meta']['today_request_count']
    Count.ost = f'осталось запросов {str(count)}'
    with open('logs/logs.txt', "a", encoding='UTF8') as log:
        log.write(f"Запрос предпринимателя по ИНН: {inn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
    with open(f'data_ip//data_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_fssp(inn):
    url = f'https://api.ofdata.ru/v2/enforcements?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    count = 100 - response['meta']['today_request_count']
    Count.ost = f'осталось запросов {str(count)}'
    with open('logs/logs.txt', "a", encoding='UTF8') as log:
        log.write(f"Запрос исполнительных производств по ИНН: {inn}.{response['meta']}. {datetime.datetime.now()}\n{count}")
    with open(f'data_fssp//data_fssp_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_gk(inn):
    url = f'https://api.ofdata.ru/v2/contracts?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    count = 100 - response['meta']['today_request_count']
    Count.ost = f'осталось запросов {str(count)}'
    with open('logs/logs.txt', "a", encoding='UTF8') as log:
        log.write(f"Запрос контрактов по ИНН: {inn}. {response['meta']}. {datetime.datetime.now()}\n{count}")
    with open(f'data_contracts//data_gk_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response