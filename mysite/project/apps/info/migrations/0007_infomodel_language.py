# Generated by Django 2.1.3 on 2019-01-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0006_auto_20190106_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='infomodel',
            name='language',
            field=models.CharField(choices=[('ru', 'russian'), ('en', 'english')], default='en', max_length=30),
        ),
    ]
