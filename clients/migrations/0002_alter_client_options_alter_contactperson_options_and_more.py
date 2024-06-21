# Generated by Django 5.0.4 on 2024-04-26 15:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Клиент', 'verbose_name_plural': 'Клиенты'},
        ),
        migrations.AlterModelOptions(
            name='contactperson',
            options={'verbose_name': 'Контактное лицо', 'verbose_name_plural': 'Контактные лица'},
        ),
        migrations.AddField(
            model_name='client',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_organizations', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
    ]
