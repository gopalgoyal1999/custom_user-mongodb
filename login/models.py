from django_mongoengine import fields,Document
from datetime import datetime
import os
from django_mongoengine.mongo_auth.models import AbstractBaseUser
from django.contrib.auth.hashers import make_password

class User(Document):
    email = fields.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = fields.StringField(max_length=50,unique=True)
    password = fields.StringField(
        max_length=128,
        verbose_name=('password')
        )
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    is_admin = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    last_login = fields.DateTimeField(default=datetime.now, verbose_name=('last login'))
    date_joined = fields.DateTimeField(default=datetime.now, verbose_name=('date joined'))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ["email"]

    #objects= UserManager()

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()
        return self

    @classmethod
    def create_user(cls, username, password, email):

        now = datetime.datetime.now()

        if email is not None:
            try:
                email_name, domain_part = email.strip().split('@', 1)
            except ValueError:
                pass
            else:
                email = '@'.join([email_name, domain_part.lower()])

        user = cls(username=username, email=email, date_joined=now)
        user.set_password(password)
        user.save()
        return user