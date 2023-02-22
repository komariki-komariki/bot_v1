import whois
from datetime import datetime
# domain_name = 'http://akcentsb.com'
def is_registered(domain_name):
    """
    A function that returns a boolean indicating
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)

def domain_data(domain_name):
    data_list = []
    new = ','
    if is_registered(domain_name):
        whois_info = whois.whois(domain_name)
        # print(whois_info)
        creat_date = whois_info.creation_date
        exp_date = whois_info.expiration_date
        reg = whois_info.registrar
        if type(exp_date) == list:
            exp_date_list = []
            newline = "; "
            for i in exp_date:
                exp_date_list.append(i.strftime('%d.%m.%Y %H:%M'))
            data_list.append(f"Домен: {whois_info.domain_name}\n"
                                 f"Зарегистрирован: {creat_date.strftime('%d.%m.%Y %H:%M')}\n"
                                 f"Оплачен до: {newline.join(exp_date_list)}\n"
                                 f"Регистратор: {reg}\nАдминистратор:{whois_info.org}")
        else:
            data_list.append(f"Домен: {whois_info.domain_name}\n"
                  f"Зарегистрирован: {creat_date.strftime('%d.%m.%Y %H:%M')}\n"
                  f"Оплачен до: {exp_date.strftime('%d.%m.%Y %H:%M')}\n"
                  f"Регистратор: {reg}\nАдминистратор: {whois_info.org}")
    return data_list

# print(domain_data(domain_name))