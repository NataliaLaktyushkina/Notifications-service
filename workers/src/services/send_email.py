import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings.email import config

mail_settings = config.settings.email_settings
# Введите свой логин и пароль от аккаунта.
mail_user = mail_settings.EMAIL_USER  # 'yourlogin@gmail.com'
mail_password = mail_settings.EMAIL_PASS  # 'your-secret-pass'

# Для подключения к серверу  требуется использовать защищённое соединение
server = smtplib.SMTP_SSL('smtp.mail.ru', 465)
server.login(mail_user, mail_password)

message = EmailMessage()
message['From'] = mail_user  # Вне зависимости от того, что вы укажете в этом поле, Gmail подставит ваши данные
message['To'] = ','.join([mail_user])  # Попробуйте отправить письмо самому себе
message['Subject'] = 'Привет!'

env = Environment(autoescape=select_autoescape(['html', 'htm', 'xml']),
                  loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))  # Указываем расположение шаблонов
template = env.get_template('mail.html')  # Загружаем нужный шаблон в переменную
# В метод render передаются данные, которые нужно подставить в шаблон
output = template.render(**{
    'title': 'Новое письмо!',
    'text': 'Произошло что-то интересное! :)',
})  # Заполняем шаблон нужной информацией
# В jinja2 также есть асинхронный рендер: template.render_async

# Для отправки HTML-письма нужно вместо метода `set_content` использовать `add_alternative` с subtype "html",
# Иначе пользователю придёт набор тегов вместо красивого письма
message.add_alternative(output, subtype='html')
server.sendmail(from_addr=mail_user,
                to_addrs=[mail_user],
                msg=message.as_string())
server.close()
