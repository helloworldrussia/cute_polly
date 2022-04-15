from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from config import EUSER

from_email = f'{EUSER}'


def get_rendered_html(template_name, context):
    if context:
        html_content = render_to_string(template_name, context)
    else:
        html_content = render_to_string(template_name)
    return html_content


def send_email(subject, html_content, text_content=None, from_email=None, recipients=[], attachments=[], bcc=[], cc=[]):
    # send email to user with attachment
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL
    if not text_content:
        text_content = ''
    email = EmailMultiAlternatives(
        subject, text_content, from_email, recipients, bcc=bcc, cc=cc
    )
    email.attach_alternative(html_content, "text/html")
    for attachment in attachments:
        # Example: email.attach('design.png', img_data, 'image/png')
        email.attach(*attachment)
    email.send()


def send_mass_mail(data_list, context):
    for data in data_list:
        template = data.pop('template')
        # context = data.pop('context')
        if context == 'invite':
            html_content = get_rendered_html(template, {"invite_url": f"http://194.58.107.50:777/email/subscribe/{data['recipients'][0]}"})
        else:
            html_content = get_rendered_html(template, context)
        data.update({'html_content': html_content})
        send_email(**data)


# message2 = {
#     'subject': 'Subject here',
#     'text_content': 'Here is the message',
#     'from_email': from_email,
#     'recipients': ['coolgrifers@gmail.com'],
#     'template': "main.html"
# }


def get_data(emails, template, subject):
    data = []
    for x in emails:
        message = {
            'subject': f'{subject}',
            'text_content': '',
            'from_email': from_email,
            'recipients': [f'{x}'],
            'template': f"{template}"
        }
        data.append(message)
    return data


message1 = {
    'subject': 'Email-Test',
    'text_content': '',
    'from_email': from_email,
    'recipients': ['erickmambergermail@yandex.ru', "erickmambergermail@gmail.com"],
    'template': "main.html"
}


def disp():
    send_mass_mail([message1])