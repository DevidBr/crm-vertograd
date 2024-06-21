from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Client(models.Model):
    """
    Модель хранит в себе описание объектов "Client". Имеет ссылку FK на модель "Manager" (поле "manager").
    """
    TYPES_CHOICES = [
        ("1", "Физ. лицо (без ИП)"),
        ("2", "ИП"),
        ("3", "Самозанятый"),
        ("4", "Организация (ООО, АО и т.д.)")
    ]
    type = models.CharField(choices=TYPES_CHOICES, max_length=100, verbose_name="Тип", blank=False)
    type_of_activity = models.CharField(max_length=255, verbose_name="Род деятельности")
    name = models.CharField(max_length=255, verbose_name="Название", blank=False)
    inn = models.CharField(max_length=12, verbose_name="ИНН", blank=True)
    city = models.CharField(max_length=255, verbose_name="Город", blank=False)
    address = models.CharField(max_length=255, verbose_name="Адрес", blank=True)
    telephone = models.CharField(max_length=15, verbose_name="Телефон организации", blank=True)
    email = models.CharField(max_length=200, verbose_name="email организации", blank=True)
    manager = models.ForeignKey(to=User,
                                on_delete=models.SET_NULL,
                                related_name="my_organizations",
                                verbose_name="Менеджер",
                                blank=True,
                                null=True)

    def __str__(self):
        return f"{self.name}. Менеджер: {self.manager}"

    def get_absolute_url(self):
        return reverse("clients:client_detail", args=[self.pk])

    def active_deals_counter(self):
        counter = 0
        for deal in self.deals.all():
            if deal.status not in ["14", "15", "16"]:
                counter += 1
        return counter

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"



class ContactPerson(models.Model):
    """
    Этот класс описывает контактное лицо. Ссылается на объект "Client" (поле "organization")
    """
    name = models.CharField(max_length=255, verbose_name="ФИО", blank=False)
    job_title = models.CharField(max_length=255, verbose_name="Должность", blank=True)
    telephone = models.CharField(max_length=25, verbose_name="телефон", blank=False)
    whatsapp = models.CharField(max_length=16, verbose_name="whatsapp", blank=True)
    telegram = models.CharField(max_length=100, verbose_name="telegram", blank=True)
    email = models.CharField(max_length=200, verbose_name="email", blank=True)
    organization = models.ForeignKey(to=Client,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name="contact_person",
                                     verbose_name="Организация")

    def __str__(self):
        return f"Контактное лицо {self.name}. Клиент: {self.organization}"

    def get_absolute_url(self):
        return reverse("clients:contact_person_detail", args=[self.pk])

    class Meta:
        verbose_name = "Контактное лицо"
        verbose_name_plural = "Контактные лица"






