# Generated by Django 2.1.3 on 2018-11-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20181125_1509'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['-id']},
        ),
        migrations.AlterField(
            model_name='profile',
            name='about_me',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='current_city',
            field=models.CharField(blank=True, max_length=99, null=True),
        ),
    ]
