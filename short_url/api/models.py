from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TargetURL(models.Model):
    full_url = models.URLField()
    short_url = models.CharField(max_length=10)
    lifetime = models.URLField()

    class Meta:
        ordering = ['-lifetime']


class UserMetaInfo(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE
    )
    ip = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=200)
