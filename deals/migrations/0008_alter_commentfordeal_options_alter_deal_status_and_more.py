# Generated by Django 5.0.4 on 2024-05-12 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0007_remove_commentfordeal_creator_commentfordeal_author'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='commentfordeal',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterField(
            model_name='deal',
            name='status',
            field=models.CharField(choices=[('1', 'Новая сделка.\nНеобходимо выбрать услугу.'), ('2', 'Выявлена потребность. Необходимо запросить стоимость у руководителя.'), ('3', 'Формируется наше предложение'), ('4', 'Предложение сформировано, разрабатываем КП'), ('5', 'КП направлено на рассмотрение заказчику'), ('6', 'Согласование условий'), ('7', 'КП согласовано, подготавливаем договор'), ('8', 'Согласование договора обеими сторонами'), ('9', 'Договор направлен на подпись'), ('10', 'Договор подписан'), ('11', 'Счет направлен заказчику. Контроль оплаты.'), ('12', 'Счет оплачен, передано в работу'), ('13', 'В работе'), ('14', 'Сделка завершена успешно. Акты подписаны.'), ('15', 'Сделка завершена без успеха'), ('16', 'Архив')], max_length=2, verbose_name='Состояние сделки'),
        ),
        migrations.CreateModel(
            name='PriceRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес объекта')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания запроса')),
                ('updated_date', models.DateTimeField(auto_now=True, verbose_name='Дата обновления запроса')),
                ('deal', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deal', to='deals.deal', verbose_name='Сделка')),
            ],
            options={
                'verbose_name': 'Запрос стоимости',
                'verbose_name_plural': 'Запросы стоимости',
            },
        ),
        migrations.CreateModel(
            name='PlantForRequestPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Неизвестно', max_length=255, verbose_name='Название растения')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='uploads/requests_price/<django.db.models.fields.related.ForeignKey>/')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='Количество')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='Высота растения')),
                ('price_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plants', to='deals.pricerequest', verbose_name='Запрос стоимости')),
            ],
            options={
                'verbose_name': 'Растение для запроса',
                'verbose_name_plural': 'Растения для запроса',
            },
        ),
    ]