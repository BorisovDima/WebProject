# Generated by Django 2.1.3 on 2019-01-06 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='status',
            field=models.CharField(choices=[('O', 'open'), ('C', 'Close')], default=None, max_length=20, verbose_name='Status'),
            preserve_default=False,
        ),
    ]
