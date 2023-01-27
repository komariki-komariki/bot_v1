import json
import requests
import datetime

from tokens import token_ofdata


def zapros(inn):
    inn = inn
    url = f'https://api.ofdata.ru/v2/company?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    with open('logs/logs.txt', "a", encoding='1251') as log:
        log.write(f"Запрос ЮЛ по ИНН: {inn}\n{response['meta']}\n{datetime.datetime.now()}\n***\n")
    with open(f'data_json_files//data_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_ogrn(ogrn):
    ogrn = ogrn
    url = f'https://api.ofdata.ru/v2/company?key={token_ofdata}&ogrn={ogrn}'
    response = requests.get(url).json()
    with open('logs/logs.txt', "a", encoding='1251') as log:
        log.write(f"Запрос ЮЛ по ОГРН: {ogrn}\n{response['meta']}\n{datetime.datetime.now()}\n***\n")
    with open(f'data_emp//data_{ogrn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_fl(inn):
    url = f'https://api.ofdata.ru/v2/person?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    with open('logs/logs.txt', "a", encoding='1251') as log:
        log.write(f"Запрос ФЛ по ИНН: {inn}\n{response['meta']}\n{datetime.datetime.now()}\n***\n")
    with open(f'data_fl//data_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response

def zapros_ip(inn):
    url = f'https://api.ofdata.ru/v2/entrepreneur?key={token_ofdata}&inn={inn}'
    response = requests.get(url).json()
    with open('logs/logs.txt', "a", encoding='1251') as log:
        log.write(f"Запрос ФЛ по ИНН: {inn}\n{response['meta']}\n{datetime.datetime.now()}\n***\n")
    with open(f'data_ip//data_{inn}.json', 'w') as f:
        json.dump(response, f)
    return response
