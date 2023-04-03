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
# zapros_fin('7706184578')

def analiz():
  with open(f'data_fin//data_7706184578.json', 'r') as f:
    fin_data = json.load(f)
    if '1530' in fin_data['data']['2021']:
      future_earnings = fin_data['data']['1530']
    else:
      future_earnings = 0
    if '1300' in fin_data['data']['2021']:
      capital_reserves = fin_data['data']['2021']['1300']
    else:
      capital_reserves = 0
  if future_earnings + capital_reserves < 0:
    return 'У компании отсутствует собственный капитал.\nСумма строк "капитал и резервы" и "доходы будущих периодов" последнего опубликованного баланса меньше 0. Это означает, что в отчетном году компания была "фундаментально" убыточна, то есть на покрытие убытков она использовала весь собственный капитал.'

def analiz_2(inn):
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
          if '1530' in fin_data['data'][str(last_year)]:
            future_earnings = fin_data['data']['1530']
          else:
            future_earnings = 0
          if '1300' in fin_data['data'][str(last_year)]:
            capital_reserves = fin_data['data'][str(last_year)]['1300']
          else:
            capital_reserves = 0
          if '2110' in reporting_last_year:
            revenue = reporting_last_year['2110']  # выручка
          else:
            revenue = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if '1600' in reporting_last_year:
            balance = reporting_last_year['1600']  # баланс (актив)
          else:
            balance = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if '2400' in reporting_last_year:
            profit = (reporting_last_year['2400'])  # чистая прибыль
            if profit < 0:
              profit = -(reporting_last_year['2400'])
              rezult = 'Чистый убыток'
            else:
              rezult = 'Чистая прибыль'
          else:
            profit = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'

          if '2110' in reporting_penultimate_year:
            penultimate_revenue = reporting_last_year['2110']  # выручка
          else:
            penultimate_revenue = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if '1600' in reporting_penultimate_year:
            penultimate_balance = reporting_last_year['1600']  # баланс (актив)
          else:
            penultimate_balance = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if '2400' in reporting_penultimate_year:
            penultimate_profit = (reporting_penultimate_year['2400'])  # чистая прибыль
            if penultimate_profit < 0:
              penultimate_profit = -(reporting_penultimate_year['2400'])
              penultimate_rezult = 'Чистый убыток'
            else:
              penultimate_rezult = 'Чистая прибыль'
          else:
            penultimate_profit = 'СВЕДЕНИЯ ОТСУТСТВУЮТ'
          if reporting_last_year['1600'] < reporting_penultimate_year['1600']:
            balance_change = f'снижение на {reporting_penultimate_year["1600"] - reporting_last_year["1600"]} рублей'
          elif reporting_last_year['1600'] == reporting_penultimate_year['1600']:
            balance_change = 'изменений нет'
          elif reporting_last_year["1600"] > reporting_penultimate_year["1600"]:
            balance_change = f'рост на {reporting_last_year["1600"] - reporting_penultimate_year["1600"]} рублей'
          if reporting_last_year["2110"] < reporting_penultimate_year["2110"]:
            revenue_change = f'снижение на {reporting_penultimate_year["2110"] - reporting_last_year["2110"]} рублей'
          elif reporting_last_year["2110"] == reporting_penultimate_year["2110"]:
            revenue_change = 'изменений нет'
          elif reporting_last_year["2110"] > reporting_penultimate_year["2110"]:
            revenue_change = f'рост на {reporting_last_year["2110"] - reporting_penultimate_year["2110"]} рублей'
          if reporting_last_year["2400"] < reporting_penultimate_year["2400"]:
            profit_change = f'снижение на {reporting_penultimate_year["2400"] - reporting_last_year["2400"]} рублей'
          elif reporting_last_year["2400"] == reporting_penultimate_year["2400"]:
            profit_change = 'изменений нет'
          elif reporting_last_year["2400"] > reporting_penultimate_year["2400"]:
            profit_change = f'рост на {reporting_last_year["2400"] - reporting_penultimate_year["2400"]} рублей'
          if future_earnings + capital_reserves < 0:
            analiza = 'У компании отсутствует собственный капитал.\nСумма строк "капитал и резервы" и "доходы будущих периодов" последнего опубликованного баланса меньше 0. Это означает, что в отчетном году компания была "фундаментально" убыточна, то есть на покрытие убытков она использовала весь собственный капитал.'
          else:
            analiza = ''
          return {
            'fin': f'Финансы на конец {last_year} года:\nБаланс - {balance} рублей;\nВыручка - {revenue} '
                   f'рублей;\n{rezult} - {profit} рублей.\n'
                   f'\nИзменения по отношению к {penultimate_year} году:\nБаланс: '
                   f'{balance_change};\nВыручка: {revenue_change};\nЧистая '
                   f'прибыль: {profit_change}.\n{analiza}\n'
          }
        else:
          for year in fin_data['data']:
            years.append(int(year))
          sorted_years = sorted(years)
          return {'fin': f'Финансы на конец {sorted_years[-1]} года:'}
      else:
        return {'fin': 'Сведения отсутствуют'}
  except Exception as e:
      return {'fin': f'ОШИБКА: {str(e)}'}

# zapros_fin('5262351728')
# pprint(analiz_2('4714004270'))

# with open('data_fin//data_4714004270.json', 'r') as f:
#   fin_data = json.load(f)
#   pprint(fin_data)