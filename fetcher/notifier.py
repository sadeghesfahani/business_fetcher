from django.conf.global_settings import EMAIL_HOST_USER
from django.core import mail

class Notifier:

    def __init__(self):
        self.sender = EMAIL_HOST_USER
        self.send_to = EMAIL_HOST_USER

    def notify(self):
        with mail.get_connection() as connection:
            mail.send_mail("search session finished", "please refresh the url in the panel admin", self.sender, connection=connection,
                           recipient_list=[self.send_to, ])
