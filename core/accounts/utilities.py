from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
import threading


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.pk) + text_type(timestamp) + text_type(user.is_verified)


generate_token = TokenGenerator()


class EmailThread(threading.Thread):
    def __init__(self, email_obj):
        threading.Thread.__init__(self)
        self.email = email_obj

    def run(self):
        self.email.send()
