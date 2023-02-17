from django.contrib.auth.models import AbstractUser
from django.db import models
import pytz

from config import settings


class MyUser(AbstractUser):
    address = models.CharField(max_length=150, blank=True)
    balance = models.IntegerField(default=0)
    timezone = models.CharField(max_length=3,
                                choices=[(str(number), pytz.all_timezones[number]) for number in
                                         range(0, len(pytz.all_timezones))],
                                default=str(pytz.all_timezones.index(settings.TIME_ZONE)))

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'