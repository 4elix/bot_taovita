import re
import random
import calendar
import datetime
import pandas as pd


def check_fio(value: list) -> int:
    if len(value) != 3:
        return 404


def check_email(value: str) -> int:
    regex = r'(?:[a-z]|[A-Z])+@gmail.'
    result = re.findall(regex, value)

    if len(result) == 0:
        return 404
    else:
        return 200


def manager_staff(value: str) -> tuple:
    step_first = value.split(', ')[::-1]
    step_second = step_first[0].split('_')[::-1]
    if len(step_second) == 1:
        return (False, False, True)
    else:
        step_second.pop(1)
        result = step_second[0]

        if result == '01999910':
            return (True, True, True)
        elif result == '0110':
            return (True, False, True)


def remove_code_fio(value: str) -> str:
    try:
        check_first = value.split(', ')[::-1][0].split('_')[::-1]
        if len(check_first) == 1:
            return value
        else:
            staff_code = '_' + check_first[0]
            return value.replace(staff_code, '')
    except Exception as error:
        print(f'{error} --- remove_code_fio')
        return '404'


def get_day(datetime_valur: datetime.datetime) -> str:
    first_step = str(datetime_valur).split(' ')
    second_step = first_step[0]
    day = second_step.split('-')[2]
    return day


def get_year(datetime_valur: datetime.datetime) -> str:
    first_step = str(datetime_valur).split(' ')
    second_step = first_step[0]
    year = second_step.split('-')[0]
    return year


def get_month(datetime_valur: datetime.datetime) -> str:
    first_step = str(datetime_valur).split(' ')
    second_step = first_step[0]
    month = second_step.split('-')[1]
    return month


def get_yesterday(datetime_valur: datetime.datetime) -> int:
    first_step = str(datetime_valur).split(' ')
    second_step = first_step[0]
    day = second_step.split('-')[2]
    result = int(day) - 1

    if result == 0:
        year, month, _ = first_step[0].split('-')
        year, month = int(year), int(month)
        prev_month = month - 1

        days_in_month = calendar.monthrange(year, prev_month)[1]
        return days_in_month
    else:
        return int(day) - 1


def write_excel_feedback(data: list, action: str, tg_id: int) -> str:
    data_excel = {
        'Отзыв': [],
        'Оценка': [],
        'Пользователь': [],
    }

    for item in data:
        data_excel['Отзыв'].append(item[0])
        data_excel['Оценка'].append(item[1])
        data_excel['Пользователь'].append(item[2])

    df = pd.DataFrame(data_excel)
    rand_num = random.randint(1000, 3000)
    tg_id = str(tg_id)
    first_step = tg_id[::-1][0-3]
    second_step = tg_id[0:5]
    rand_num = str(rand_num)

    path = f'media/feedback_files/отчет за {action} №{first_step+second_step+rand_num}.xlsx'

    df.to_excel(path, index=False)
    return path


def write_excel_sales_info(data: list, action: str, tg_id: int) -> str:
    data_excel = {
        'ФИО': [],
        'Номер телефона': [],
        'Общая кол-во': [],
        'Общая стоимость': [],
    }

    for item in data:
        data_excel['ФИО'].append(item[0])
        data_excel['Номер телефона'].append(item[1])
        data_excel['Общая кол-во'].append(item[2])
        data_excel['Общая стоимость'].append(item[3])

    df = pd.DataFrame(data_excel)
    rand_num = random.randint(1000, 3000)
    tg_id = str(tg_id)
    first_step = tg_id[::-1][0-3]
    second_step = tg_id[0:5]
    rand_num = str(rand_num)
    path = f'media/sales_info/отчет за {action} №{first_step+second_step+rand_num}.xlsx'

    df.to_excel(path, index=False)
    return path


def update_phone_number(phone_number: str) -> str:
    if phone_number[0] == '+':
        return phone_number
    else:
        new_phone_number = '+' + phone_number
        return new_phone_number
