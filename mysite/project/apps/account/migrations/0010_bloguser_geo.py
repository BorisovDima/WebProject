# Generated by Django 2.1.3 on 2019-01-07 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20190105_2206'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='geo',
            field=models.CharField(default='RU', max_length=100),
        ),
    ]
