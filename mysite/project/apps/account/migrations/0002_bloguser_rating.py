# Generated by Django 2.1.3 on 2018-12-06 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
