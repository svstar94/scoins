# Generated by Django 3.1.4 on 2021-01-12 22:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounting',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book', to=settings.AUTH_USER_MODEL),
        ),
    ]
