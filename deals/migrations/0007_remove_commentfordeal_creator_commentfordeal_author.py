# Generated by Django 5.0.4 on 2024-05-05 16:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0006_commentfordeal_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentfordeal',
            name='creator',
        ),
        migrations.AddField(
            model_name='commentfordeal',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='my_comments', to=settings.AUTH_USER_MODEL, verbose_name='author'),
        ),
    ]