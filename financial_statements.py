import json
from pprint import pprint
from ofdata_api import zapros_fin

def fin_stat(inn):
  try:
    years = []
    zapros_fin(inn)
    with open(f'data_fin//data_{inn}.json', 'r') as f:
      fin_data = json.load(f)
      if len(fin_data['data']) > 0:
        if len(fin_data['data']) > 1:
          for year in fin_data['data']:
              years.append(int(year))
          sorted_years = sorted(years)
          last_year = sorted_years[-1]
          penultimate_year = sorted_years[-2]
          reporting_last_year = (fin_data['data'][str(last_year)])
          reporting_penultimate_year = (fin_data['data'][str(penultimate_year)])
          if '2110' in reporting_last_year:
            revenue = reporting_last_year['2110']#выручка
          else:
            revenue = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if '1600' in reporting_last_year:
            balance = reporting_last_year['1600']#баланс (актив)
          else:
            balance = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if '2400' in reporting_last_year:
            profit = (reporting_last_year['2400'])#чистая прибыль
            if profit < 0:
              profit = -(reporting_last_year['2400'])
              rezult = 'Чистый убыток'
            else:
              rezult = 'Чистая прибыль'
          else:
            profit = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          return {'fin': f'Финансы на конец {last_year} года:\nБаланс - {balance} рублей;\nВыручка - {revenue} '
                         f'рублей;\n{rezult} - {profit} рублей.'}
        else:
          for year in fin_data['data']:
              years.append(int(year))
          sorted_years = sorted(years)
          return {'fin': f'Финансы на конец {sorted_years[-1]} года:'}
      else:
        return {'fin': 'Сведения отсутствуют'}
  except Exception as e:
      return {'fin': f'ОШИБКА: {str(e)}'}



# pprint(fin_stat('5505009406'))