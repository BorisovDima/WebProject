# Generated by Django 2.1.3 on 2018-12-26 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20181225_1856'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='email'),
        ),
    ]
