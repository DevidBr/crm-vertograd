# Generated by Django 5.0.4 on 2024-06-03 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0018_alter_commercialoffer_deal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commercialoffer',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='uploads/documents_copy/commercial_offer/%Y/%m/%d/', verbose_name='Коммерческое предложение'),
        ),
    ]
