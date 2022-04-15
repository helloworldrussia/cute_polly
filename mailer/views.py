import threading
import time

from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from config import EUSER
from mailer.backend import disp
from mailer.mixins import dispatcher, read_emails, save_new_emails,get_list_from_qs
from mailer.models import Address

fs = FileSystemStorage(location='static/users_files')
fs_for_templates = FileSystemStorage(location='mailer/templates/')


def client_ask(request, email, type):
    # email = request.GET['email']
    # type = request.GET['type']
    if type == 'subscribe' or type == 'unsubscribe':
        try:
            obj = Address.objects.get(email=email)
            obj.status = type
            obj.save()
            if type == 'subscribe':
                return render(request, 'subscribe.html')
            if type == 'unsubscribe':
                return render(request, 'unsubscribe.html')
        except:
            return HttpResponse(404)
    else:
        return HttpResponse(404)


class IndexView(TemplateView):
    template_name = 'index.html'

    def post(self, args):
        print(self.request.FILES, self.request.POST)
        # цепляем файлы и данные из формы
        # emails = self.request.FILES['emails']
        template = self.request.FILES['template']
        subject, callback = self.request.POST['subject'], self.request.POST['callback']

        # сохраняем
        # fs.save(emails.name, emails)
        fs_for_templates.save(template.name, template)

        emails_list = Address.objects.filter(status='subscribe').values('email')
        emails_list = get_list_from_qs(emails_list)
        # # читаем файл со списком адресов
        # emails_list = read_emails(emails.name)
        #
        # # начинаем рассылку
        thread = threading.Thread(target=dispatcher, args=(emails_list, template.name, subject, callback, False))
        thread.start()
        # расчитываем время работы и даем ответ
        integer = int(len(emails_list) / 70)
        if integer < 1:
            integer = 1
        return HttpResponse(f'Рассылка началась. Примерное время завершения: {integer} мин. Ответ придет на {callback}')


def add_emails(request):
    if request.method == 'GET':
        return render(request, 'db.html')
    if request.method == 'POST':
        file = request.FILES['emails']
        fs.save(file.name, file)
        emails = read_emails(file.name)
        print(emails)
        message = save_new_emails(emails)
        # th = threading.Thread(target=save_new_emails, args=(emails,))
        # th.start()
        return render(request, 'db.html', {'message': message})


def invite(request):
    if request.method == 'GET':
        return render(request, 'invite.html')
    if request.method == 'POST':
        subject = request.POST['subject']
        callback = request.POST['callback']
        message = ''
        emails_list = Address.objects.filter(status='new').values('email')
        emails_list = get_list_from_qs(emails_list)
        print(emails_list)
        thread = threading.Thread(target=dispatcher, args=(emails_list, 'welcome.html', subject, callback, 'invite'))
        thread.start()
        # расчитываем время работы и даем ответ
        integer = int(len(emails_list) / 70)
        if integer < 1:
            integer = 1
        message = f'Рассылка началась. Примерное время завершения: {integer} мин. Ответ придет на {callback}'
        return render(request, 'invite.html', {'message': message})


# olga_list = ['arkatinka@gmail.com', 'New.superday@gmail.com', 'bartosevicdia`na@gmail.com',
#              'Helen.kokorina@gmail.com', 'Ernesta.laurinavice@gmail.com ', 'Mause312@mail.ru',
#              'larisa-leven@mail.ru', 'alvina-k@yandex.ru', 'manna17@mail.ru', '', 'Nltutova@gmail.com',
#              'Jan-ganka@yandex.ru ', 'nafanailovamaria2019@gmail.com', 'Priymenka@gmail.com', 'akameneva376@gmail.com',
olga_list = ['erickmambergermail@yandex.ru', 'erickmambergermail@gmail.com', 'polina0408polina@gmail.com']

#olga_text = 'Здравствуйте!\nВы получили тестовое письмо от нашего нового почтового сервиса.\nМы проверяем как он работает. Пожалуйста, пришлите в ответ что-нибудь позитивное и отметьте письмо как важное (добавить в избранное, закладки).\n(смаилик или 1-2 предложения со словами "круто", "спасибо" итд)\n\nЕсли вас не затруднит, то сообщите на адрес erickmambergermail@gmail.com попало ли письмо в спам, раздел промо-акции\nПомимо gmail можете сообщить это в телеграм @helloworldrussia.\nСпасибо!'
olga_text = 'Привет, это очередная проверка. Смотрим кастомные заголовки.'
def test(request):
    # html_message = render_to_string(f'good.html')
    # plain_message = strip_tags(html_message)
    from_email = f'{EUSER}'
    subject = 'Проверка связи'
    # # send_mail(subject, plain_message, from_email, to, html_message=html_message)
    # send_mail('Checking DKIM, TLS and SPF', 'I promise, thats last for today xD. Send something back)', 'Cute Polly <root@izdatelstvo.skrebeyko.ru>',
    #           to)
    # return HttpResponse(200)
    all_messages = []
    for x in olga_list:
        message = EmailMessage(subject, olga_text, from_email, [x], headers={
            "List-Unsubscribe": "<https://izdatelstvo.skrebeyko.ru/>"
        })
        all_messages.append(message)
    # send_mass_mail(all_messages)
    for x in all_messages:
        x.send()
    return HttpResponse(200)


