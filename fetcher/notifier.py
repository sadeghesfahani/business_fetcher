from django.core import mail

class Notifier:

    def __init__(self):
        self.sender = "betatool@alcatech.de"
        self.send_to = "betatool@alcatech.de"

    def notify(self):
        with mail.get_connection() as connection:
            mail.send_mail("search session finished", "please refresh the url in the panel admin", self.sender, connection=connection,
                           recipient_list=[self.send_to, ])
