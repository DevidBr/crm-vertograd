from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from clients.models import Client
from services.models import Service


class Deal(models.Model):
    STATUS_CHOICES = [
        ("1", "Новая сделка.\nНеобходимо выбрать услугу."),
        ("2", "Выявлена потребность. Необходимо запросить стоимость у руководителя."),
        ("3", "Запрос стоимости отправлен. Ожидание ответа руководителя."),
        ("4", "Стоимость утверждена. Необходимо подготовить КП."),
        ("5", "КП сохранено. Необходимо направить КП клиенту."),
        ("6", "Ведение переговоров на тему заключения договора."),
        ("7", "Договор запрошен. Ожидание ответа руководителя."),
        ("8", "Договор подготовлен. Согласование с клиентом."),
        ("9", "Подписание договора."),
        ("10", "Договор подписан обеими сторонами. Необходимо сохранить скан."),
        ("11", "Ожидаем счет от руководителя."),
        ("12", "Счет выставлен, направлен клиенту. Контроль оплаты"),
        ("13", "Счет оплачен. Передать в работу."),
        ("14", "В работе"),
        ("15", "Сделка завершена успешно"),
        ("16", "Сделка завершена без успеха"),
        ("17", "Архив")
    ]

    organization = models.ForeignKey(to=Client,
                                     on_delete=models.SET_NULL,
                                     null=True,
                                     blank=True,
                                     related_name="deals",
                                     verbose_name="Организация")

    manager = models.ForeignKey(to=User,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="my_deals",
                                verbose_name="Менеджер")

    service = models.ForeignKey(to=Service,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name="deals",
                                verbose_name="Услуга")

    cost_price = models.DecimalField(max_digits=8,
                                     decimal_places=2,
                                     verbose_name="Себестоимость сделки",
                                     blank=True,
                                     null=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name="Стоимость сделки",
                                blank=True,
                                null=True)

    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата создания сделки")
    updated_date = models.DateTimeField(auto_now=True,
                                        blank=True,
                                        null=True,
                                        verbose_name="Дата последнего изменения сделки")
    completion_date = models.DateTimeField(verbose_name="Дата завершения сделки",
                                           blank=True,
                                           null=True)

    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=2,
                              verbose_name="Состояние сделки")


    act_number = models.CharField(max_length=255,
                                  verbose_name="Номер акта",
                                  blank=True,
                                  null=True)

    act_image = models.ImageField(upload_to="uploads/documents_copy/acts/%Y/%m/%d/",
                                  verbose_name="Скан акта",
                                  blank=True,
                                  null=True)

    # TODO: Убрать blank=True
    description = models.TextField(verbose_name="Общее описание сделки", blank=True)

    class Meta:
        verbose_name = "Сделка"
        verbose_name_plural = "Сделки"

    def __str__(self):
        if self.organization != None:
            return f"Сделка №{self.pk}: Клиент: {self.organization.name}."
        else:
            return f"Сделка №{self.pk}."

    def get_net_profit(self):
        return float(self.price) - float(self.cost_price)

    def get_absolute_url(self):
        return reverse("deals:deal_detail", args=[self.pk])


class CommentForDeal(models.Model):
    deal = models.ForeignKey(to=Deal,
                             on_delete=models.CASCADE,
                             related_name="comments",
                             verbose_name="Сделка",
                             null=True,
                             blank=True)

    text = models.TextField(verbose_name="Текст комментария")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Изменен")
    author = models.ForeignKey(to=User,
                               on_delete=models.SET_NULL,
                               blank=True,
                               null=True,
                               verbose_name="author",
                               related_name="my_comments")

    def __str__(self):
        return f"{self.deal}, {self.updated_date}: {self.text}"

    class Meta:
        ordering = ["-created_date"]


class PriceRequest(models.Model):
    PRICE_REQUEST_STATUS_CHOICES = [
        ("1", "Ожидание оценки"),
        ("2", "Оценка завершена")
    ]

    address = models.CharField(max_length=255, verbose_name="Адрес объекта")
    deal = models.OneToOneField(to=Deal, related_name="price_request", on_delete=models.CASCADE, verbose_name="Сделка")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания запроса")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления запроса")

    comment_from_manager = models.TextField(verbose_name="Комментарий от менеджера")
    comment_from_director = models.TextField(verbose_name="Комментарий от руководителя")

    status = models.CharField(choices=PRICE_REQUEST_STATUS_CHOICES, default="1", verbose_name="Статус запроса",
                              max_length=1)

    def __str__(self):
        return f"Запрос стоимости №{self.pk}: Сделка №{self.deal.pk}"

    def get_absolute_url(self):
        return reverse(viewname="deals:price_request_detail", args=[self.pk])

    class Meta:
        verbose_name = "Запрос стоимости"
        verbose_name_plural = "Запросы стоимости"


class PlantForPriceRequest(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название растения", default="Неизвестно")

    price_request = models.ForeignKey(to=PriceRequest,
                                      verbose_name="Запрос стоимости",
                                      on_delete=models.CASCADE,
                                      related_name="plants")

    photo = models.ImageField(upload_to=f"uploads/requests_price/{price_request}/", blank=True, null=True)
    quantity = models.IntegerField(verbose_name="Количество", blank=True, null=True)
    height = models.FloatField(verbose_name="Высота растения", blank=True, null=True)

    def __str__(self):
        return f"Растение: {self.name} для запроса стоимости {self.price_request}"

    class Meta:
        verbose_name = "Растение для запроса"
        verbose_name_plural = "Растения для запроса"


class CommercialOffer(models.Model):
    counter_number = models.PositiveIntegerField(verbose_name="№")
    deal = models.ForeignKey(to=Deal,
                             on_delete=models.CASCADE,
                             related_name="commercial_offers",
                             verbose_name="Сделка",
                             null=True,
                             blank=True)

    number = models.CharField(max_length=20, verbose_name="№ исх.", unique=True)
    date = models.DateField(verbose_name="от: ")
    image = models.FileField(upload_to="uploads/documents_copy/commercial_offer/%Y/%m/%d/",
                              verbose_name="Коммерческое предложение",
                              blank=True,
                              null=True)
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="commercial_offers")

    class Meta:
        verbose_name = "Коммерческое предложение"
        verbose_name_plural = "Коммерческие предложения"


class ContractRequest(models.Model):
    CONTRACT_REQUEST_STATUS_CHOICES = [
        ("1", "Ожидание договора"),
        ("2", "Проект договора готов")
    ]
    deal = models.ForeignKey(to=Deal,
                             on_delete=models.CASCADE,
                             related_name="contract_requests",
                             verbose_name="Запрос контракта")

    creator = models.ForeignKey(to=User,
                                on_delete=models.PROTECT,
                                related_name="contract_requests")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Запрос создан")
    description = models.TextField(verbose_name="Описание условий договора")
    status = models.CharField(choices=CONTRACT_REQUEST_STATUS_CHOICES,
                              default="1",
                              verbose_name="Статус",
                              max_length=2)

    def get_absolute_url(self):
        return reverse(viewname="deals:contract_request_detail", args=[self.pk])

    class Meta:
        verbose_name = "Запрос контракта"
        verbose_name_plural = "Запросы контрактов"


class Contract(models.Model):
    CONTRACT_STATUS_CHOICES = [
        ("1", "Подготовка и согласование"),
        ("2", "Внесение изменений"),
        ("3", "Подписан обеими сторонами"),
        ("4", "Оплачен и передан в работу"),
    ]

    deal = models.ForeignKey(to=Deal,
                             on_delete=models.CASCADE,
                             related_name="contracts",
                             verbose_name="Сделка")

    contract_number = models.CharField(max_length=155, verbose_name="Номер договора")
    contract_date = models.DateField(verbose_name="Дата договора")
    contract_text = models.FileField(upload_to="uploads/documents_copy/contract_texts/%Y/%m/%d/",
                                     verbose_name="Текст договора",
                                     blank=True,
                                     null=True)
    contract_image = models.FileField(upload_to="uploads/documents_copy/contract_images/%Y/%m/%d/",
                                      verbose_name="Копия подписанного договора",
                                      blank=True,
                                      null=True)

    status = models.CharField(choices=CONTRACT_STATUS_CHOICES, verbose_name="Статус контракта", max_length=2)


class Bill(models.Model):
    BILL_STATUS_CHOICES = [
        ("1", "Выставлен, не оплачен"),
        ("2", "Оплачен")
    ]

    status = models.CharField(choices=BILL_STATUS_CHOICES, verbose_name="Статус", max_length=2)

    bill_number = models.CharField(max_length=155, verbose_name="Номер счета")
    bill_date = models.DateField(verbose_name="Дата счета")
    bill_image = models.FileField(upload_to="uploads/documents_copy/bill_images/%Y/%m/%d/",
                                  verbose_name="Копия счета",
                                  blank=True,
                                  null=True)

    contract = models.ForeignKey(to=Contract,
                                 on_delete=models.CASCADE,
                                 related_name="bills",
                                 verbose_name="Договор")


class Act(models.Model):
    ACT_STATUS_CHOICES = [
        ("1", "Выставлен, но не подписан"),
        ("2", "Подписан")
    ]

    status = models.CharField(choices=ACT_STATUS_CHOICES,
                              verbose_name="Статус",
                              default="1",
                              max_length=2)

    contract = models.OneToOneField(to=Contract,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True,
                                    related_name="act",
                                    verbose_name="Договор")

    act_number = models.CharField(max_length=155, verbose_name="Номер акта")
    act_date = models.DateField(verbose_name="Дата акта")

    act_text = models.FileField(upload_to="uploads/documents_copy/act_texts/%Y/%m/%d/",
                                verbose_name="Текст акта",
                                blank=True,
                                null=True)
    act_image = models.FileField(upload_to="uploads/documents_copy/act_texts/%Y/%m/%d/",
                                 verbose_name="Копия подписанного акта",
                                 blank=True,
                                 null=True)
