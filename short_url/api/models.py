from django.db import models


class TargetURL(models.Model):
    full_url = models.URLField()
    short_url = models.CharField(max_length=7)
    lifetime = models.URLField()

    class Meta:
        ordering = ['-lifetime']
