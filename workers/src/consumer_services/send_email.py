import smtplib
from email.message import EmailMessage
from typing import List, Union

from jinja2 import Template

from settings.email import config
from worker_models.events import Templates


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

    def add_header(self, receivers: List[str], msg_subject: str) -> None:  # type: ignore
        self.message['From'] = self.mail_user  # Вне зависимости от того, что вы укажете в этом поле, Gmail подставит ваши данные
        self.message['To'] = ','.join(receivers)  # Попробуйте отправить письмо самому себе
        self.message['Subject'] = msg_subject

    def add_template(self, template: Templates,
                     title: str, text: str) -> None:
        template = Template(template.html)

        # В метод render передаются данные, которые нужно подставить в шаблон
        self.output = template.render(**{
            'title': title,
            'text': text,
        })  # Заполняем шаблон нужной информацией
        # В jinja2 также есть асинхронный рендер: template.render_async

    def send_msg(self, receivers: List[str]) -> Union[None, str]:  # type: ignore
        # Для отправки HTML-письма нужно вместо метода `set_content` использовать `add_alternative` с subtype "html",
        # Иначе пользователю придёт набор тегов вместо красивого письма
        self.message.add_alternative(self.output, subtype='html')
        try:
            self.server.sendmail(from_addr=self.mail_user,
                                 to_addrs=receivers,
                                 msg=self.message.as_string())
        except smtplib.SMTPDataError:
            return 'user not found'
        self.server.close()


def main(receivers: list, subject: str, title: str,
         template: str, text: str) -> None:
    email_sender = EmailSender()
    email_sender.add_header(receivers=receivers,
                            msg_subject=subject)
    email_sender.add_template(template=template,
                              title=title,
                              text=text)
    email_sender.send_msg(receivers=receivers)


if __name__ == '__main__':
    main(receivers=['education_tests@mail.ru'],
         subject='Registration',
         title='Registration complete',
         template='mail.html',
         text='Main text for debug')
