import os
import smtplib
from email.message import EmailMessage
from jinja2 import Environment, FileSystemLoader, select_autoescape
from settings.email import config


class EmailSender:

    def __init__(self) -> None:
        """mail settings"""
        mail_settings = config.settings.email_settings
        smtp_settings = config.settings.smtp_settings
        self.mail_user = mail_settings.EMAIL_USER  # 'yourlogin@gmail.com'
        self.mail_password = mail_settings.EMAIL_PASS  # 'your-secret-pass'

        # Для подключения к серверу  требуется использовать защищённое соединение
        self.server = smtplib.SMTP_SSL(host=smtp_settings.SMTP_HOST,
                                       port=smtp_settings.SMTP_PORT)
        self.server.login(self.mail_user, self.mail_password)
        self.message = EmailMessage()
        self.output = ''

    def add_header(self, receivers: list[str], msg_subject: str) -> None:  # type: ignore
        self.message['From'] = self.mail_user  # Вне зависимости от того, что вы укажете в этом поле, Gmail подставит ваши данные
        self.message['To'] = ','.join(receivers)  # Попробуйте отправить письмо самому себе
        self.message['Subject'] = msg_subject

    def add_template(self, template_name: str,
                     title: str, text: str) -> None:
        env = Environment(autoescape=select_autoescape(['html', 'htm', 'xml']),
                          loader=FileSystemLoader(f'{os.path.dirname(__file__)}'))  # Указываем расположение шаблонов
        template = env.get_template(template_name)  # 'mail.html'
        # В метод render передаются данные, которые нужно подставить в шаблон
        self.output = template.render(**{
            'title': title,
            'text': text,
        })  # Заполняем шаблон нужной информацией
        # В jinja2 также есть асинхронный рендер: template.render_async

    def send_msg(self, receivers: list[str]) -> None:  # type: ignore
        # Для отправки HTML-письма нужно вместо метода `set_content` использовать `add_alternative` с subtype "html",
        # Иначе пользователю придёт набор тегов вместо красивого письма
        self.message.add_alternative(self.output, subtype='html')
        self.server.sendmail(from_addr=self.mail_user,
                             to_addrs=receivers,
                             msg=self.message.as_string())
        self.server.close()


def main() -> None:
    email_sender = EmailSender()
    email_sender.add_header(receivers=['education_tests@mail.ru'],
                            msg_subject='A letter from me!')
    email_sender.add_template(template_name='mail.html',
                              title='This is title',
                              text='Looong text')
    email_sender.send_msg(receivers=['education_tests@mail.ru'])


if __name__ == '__main__':
    main()
