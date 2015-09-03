from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import TrickerManager


class Tricker(AbstractBaseUser):
    email = models.EmailField(unique=True, db_index=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    objects = TrickerManager()

    class Meta:
        verbose_name = "Tricker"
        verbose_name_plural = "Trickers"

    def get_full_name(self):
        return self.email

    def __unicode__(self):
        return self.email
