# Generated by Django 5.0.4 on 2024-06-03 17:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0022_contractrequest_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='contract_image',
        ),
        migrations.RemoveField(
            model_name='deal',
            name='contract_number',
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(max_length=155, verbose_name='Номер договора')),
                ('contract_date', models.DateField(verbose_name='Дата договора')),
                ('contract_text', models.FileField(blank=True, null=True, upload_to='uploads/documents_copy/contract_texts/%Y/%m/%d/', verbose_name='Текст договора')),
                ('contract_image', models.FileField(blank=True, null=True, upload_to='uploads/documents_copy/contract_images/%Y/%m/%d/', verbose_name='Копия подписанного договора')),
                ('status', models.CharField(choices=[('1', 'Подготовка и согласование'), ('2', 'Подписан обеими сторонами'), ('3', 'Оплачен и передан в работу')], max_length=2, verbose_name='Статус контракта')),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contracts', to='deals.deal')),
            ],
        ),
    ]
