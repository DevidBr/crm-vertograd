# Generated by Django 5.0.4 on 2024-05-01 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0002_rename_deal_statuses_deal_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='contract_image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/documents_copy/contracts/%Y/%m/%d/', verbose_name='Скан договора'),
        ),
    ]
