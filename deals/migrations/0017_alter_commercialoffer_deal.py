# Generated by Django 5.0.4 on 2024-06-03 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0016_alter_commercialoffer_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialoffer',
            name='deal',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commercial_offer', to='deals.deal', verbose_name='Сделка'),
        ),
    ]