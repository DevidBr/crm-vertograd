# Generated by Django 5.0.4 on 2024-05-12 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0008_alter_commentfordeal_options_alter_deal_status_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlantForRequestPrice',
            new_name='PlantForPriceRequest',
        ),
    ]
