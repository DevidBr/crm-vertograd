from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")

    def __str__(self):
        return self.name
