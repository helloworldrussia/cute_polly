import threading
import time
from django.core.mail import send_mail, send_mass_mail, EmailMessage
from django.core.mail.backends.smtp import EmailBackend
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic import TemplateView
from config import EUSER
from mailer.backend import disp
from mailer.mixins import dispatcher, read_emails, save_new_emails, get_list_from_qs, save_or_update_email, \
    check_session, email_validator
from mailer.models import Address

fs = FileSystemStorage(location='static/users_files')
fs_for_templates = FileSystemStorage(location='mailer/templates/')


def client_ask(request, email, type):
    # email = request.GET['email']
    # type = request.GET['type']
    print(email, type)
    if type == 'subscribe' or type == 'unsubscribe' and email != '' and email is not None:
        try:
            obj = Address.objects.get(email=email)
            obj.status = type
            obj.save()
        except:
            obj = Address()
            obj.email = email
            obj.status = type
            obj.save()

        if type == 'subscribe':
            return render(request, 'core/subscribe.html')
        if type == 'unsubscribe':
            return render(request, 'core/unsubscribe.html')
    else:
        return HttpResponse(404)


class IndexView(TemplateView):
    template_name = 'core/index.html'

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
        message = f'Рассылка началась. Примерное время завершения: {integer} мин. Ответ придет на {callback}'
        return render(self.request, 'core/index.html', {'message': message})


def add_emails(request):
    if request.method == 'GET':
        return render(request, 'core/db.html')
    if request.method == 'POST':
        file = request.FILES['emails']
        fs.save(file.name, file)
        emails = read_emails(file.name)
        print(emails)
        message = save_new_emails(emails)
        # th = threading.Thread(target=save_new_emails, args=(emails,))
        # th.start()
        return render(request, 'core/db.html', {'message': message})


def invite(request):
    if request.method == 'GET':
        return render(request, 'core/invite.html')
    if request.method == 'POST':
        subject = request.POST['subject']
        callback = request.POST['callback']
        message = ''
        emails_list = Address.objects.filter(status='new').values('email')
        emails_list = get_list_from_qs(emails_list)
        print(emails_list)
        thread = threading.Thread(target=dispatcher, args=(emails_list, 'core/welcome.html', subject, callback, 'invite'))
        thread.start()
        # расчитываем время работы и даем ответ
        integer = int(len(emails_list) / 70)
        if integer < 1:
            integer = 1
        message = f'Рассылка началась. Примерное время завершения: {integer} мин. Ответ придет на {callback}'
        return render(request, 'core/invite.html', {'message': message})


def inv_form(request):
    if request.method == 'POST':
        if check_session(request.session):
            request.session['invite_form_mode'] = ''
            try:
                email = request.POST['email']
            except:
                return redirect('https://izdatelstvo.skrebeyko.ru')

        email = request.POST['email']
        # если поле имейла оставили пустым, выбрасываем сообщение об ошибке
        if email == '':
            return render(request, 'core/inv_form.html', {"message": "Вы отправили нам пустую строку"})
        # проверяем введенный имейл на существование, аналогично выбрасываем ошибку при ошибке))
        if not email_validator(email):
            url = f'https://mail.izdatelstvo.skrebeyko.ru/email/subscribe/{email}'
            return render(request, 'core/inv_form.html', {"message": f"Адрес почты {email} определен как несуществующий."
                                                                     " Пожалуйста, проверьте введенные данные.\n"
                                                                     "Попробуйте исправить или ввести другой email.\n\n"
                                                                     "Если адрес почты введен верно, перейдите "
                                                                     f"по ссылке.",
                                                          "url": url})
        if save_or_update_email(email):
            request.session['invite_form_mode'] = '1'
            return render(request, 'core/inv_success.html', {"user_email": email})

    if request.method == 'GET':
        return render(request, 'core/inv_form.html')
