# Generated by Django 3.1.4 on 2021-01-04 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_news_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='writer',
        ),
    ]
