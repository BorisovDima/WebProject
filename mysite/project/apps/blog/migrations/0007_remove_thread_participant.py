# Generated by Django 2.1.3 on 2018-12-12 18:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20181211_2053'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='participant',
        ),
    ]
