import random
import time
from datetime import datetime

from django.core import mail
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from config import EUSER, EPASSWORD
from mailer.backend import get_data, send_mass_mail
from mailer.models import Address

fs = FileSystemStorage(location='static/users_files')
fs_for_templates = FileSystemStorage(location='mailer/templates/')


# функция диспетчер, распределяет задачи, необходимые для выполнения рассылки
def dispatcher(emails, template, subject, callback, context):

    # запускаем отправку по 90 писем. ждем минуту и снова, пока все не отправим. обход спама v1
    result = []
    # превращаем список в список словарей - объектов писем
    emails = get_data(emails, template, subject)
    print(emails)

    # try:
    while True:
        if emails:
            count = random.randint(70, 89)
            if context == 'invite':
                send_mass_mail(emails[:count], context)
            else:
                send_mass_mail(emails[:count], context)
            del emails[:count]
            print('****'*random.randint(2, 4))
            time.sleep(random.randint(60, 70))
        else:
            break
        print('Sending GOOD')
        send_good('База Адресов', callback)
    # except Exception as error:
    #     #send_bad(emails_file, callback, result, error)
    #     print(f'Very BAAAD {error}')
    # # удаляем файл
    if context != 'invite':
        fs_for_templates.delete(template)


# читает имейлы из файла. всегда должны быть в файле столбцом
def read_emails(emails_file):
    emails = []
    with open(f'static/users_files/{emails_file}', encoding='utf-8') as f:

        # f = open(f'static/users_files/{emails_file}', 'r')
        try:
            while True:
                # считываем строку
                line = f.readline()
                # прерываем цикл, если строка пустая
                if not line:
                    break
                # выводим строку
                emails.append(line.strip())
        finally:
            f.close()
    fs.delete(emails_file)
    return emails


# получив все необходимое, принимается за отправку самих писем и письма с отчетом (автору по callback)
def send(emails, template, subject): #, callback):
    from_email = EUSER

    try:
        html_message = render_to_string(f'{template}')
        plain_message = strip_tags(html_message)
        to = emails

        mail.send_mail(subject, plain_message, from_email, to, html_message=html_message)
        return 'good'
    except Exception as error:
        return error


# Access message to owner
def send_good(emails_file, callback):
    html_message = render_to_string(f'core/good.html')
    plain_message = strip_tags(html_message)
    mail.send_mail(f'Отчет о рассылке по {emails_file}', f'Рассылка прошла успешно [{datetime.now()}]', EUSER, [callback])
                   #html_message=html_message)


# Error warning
def send_bad(emails_file, callback, result, error):
    mail.send_mail(f'Ошибка в рассылке по {emails_file}', f'Internal Error:\n\n{error}\n\n{result}', EUSER, [callback])


def save_new_emails(emails):
    # all = Address.objects.all().values('email')
    bad = 0
    print(all)
    for email in emails:
        try:
            test = Address.objects.get(email=email)
            bad += 1
            continue
        except Exception as ex:
            print(ex)
            obj = Address()
            obj.email = email
            obj.save()
    good = len(emails) - bad
    return f'Успешно: {good} Дублей найдено {bad}'
    # return 'TEST'


def get_list_from_qs(qs):
    all = qs
    emails = []
    for x in all:
        print(x)
        emails.append(x['email'])
    return emails