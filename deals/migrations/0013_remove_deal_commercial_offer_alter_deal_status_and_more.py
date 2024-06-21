# Generated by Django 5.0.4 on 2024-05-31 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0012_deal_commercial_offer_alter_deal_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='commercial_offer',
        ),
        migrations.AlterField(
            model_name='deal',
            name='status',
            field=models.CharField(choices=[('1', 'Новая сделка.\nНеобходимо выбрать услугу.'), ('2', 'Выявлена потребность. Необходимо запросить стоимость у руководителя.'), ('3', 'Запрос стоимости отправлен. Ожидание ответа руководителя.'), ('4', 'Стоимость утверждена. Необходимо подготовить КП.'), ('5', 'КП сохранено. Необходимо направить КП клиенту.'), ('6', 'Согласование условий'), ('7', 'КП согласовано, подготавливаем договор'), ('8', 'Согласование договора обеими сторонами'), ('9', 'Договор направлен на подпись'), ('10', 'Договор подписан'), ('11', 'Счет направлен заказчику. Контроль оплаты.'), ('12', 'Счет оплачен, передано в работу'), ('13', 'В работе'), ('14', 'Сделка завершена успешно. Акты подписаны.'), ('15', 'Сделка завершена без успеха'), ('16', 'Архив')], max_length=2, verbose_name='Состояние сделки'),
        ),
        migrations.CreateModel(
            name='CommercialOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='№ исх.')),
                ('date', models.DateField(verbose_name='от: ')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/documents_copy/commercial_offer/%Y/%m/%d/', verbose_name='Коммерческое предложение')),
                ('deal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='commercial_offer', to='deals.deal', verbose_name='Сделка')),
            ],
        ),
    ]