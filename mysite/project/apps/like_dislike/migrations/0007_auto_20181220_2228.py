# Generated by Django 2.1.3 on 2018-12-20 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('like_dislike', '0006_auto_20181212_1804'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribe',
            options={'ordering': ['-id']},
        ),
    ]
