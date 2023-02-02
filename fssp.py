import json
from datetime import datetime
from ofdata_api import zapros_fssp


def fssp(inn):
    try:
        zapros_fssp(inn)
        with open(f'data_fssp/data_fssp_{inn}.json', 'r', encoding='UTF8') as f:
            json_file = json.load(f)
            if json_file["data"]["ОбщКолич"] > 0:
                return {
                    'fssp': f'По состоянию на {datetime.now().strftime("%d.%m.%Y")} в отношении {json_file["company"]["НаимСокр"]} '
                            f'ведется {json_file["data"]["ОбщКолич"]}  '
                            f'исполнительных производств на общую сумму '
                            f'{json_file["data"]["ОбщСум"]} рублей'
                }
            else:
                return {
                    'fssp': f'По состоянию на {datetime.now().strftime("%d.%m.%Y")} в отношении {json_file["company"]["НаимСокр"]} '
                            f'исполнительные производства не ведутся'
                }
    except Exception as e:
        return {'fssp': f'ОШИБКА: {str(e)}'}

# zapros_fssp('7830000426')
# fssp('data_fssp/data_fssp_9703024280.json')