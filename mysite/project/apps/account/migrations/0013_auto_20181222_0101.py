# Generated by Django 2.1.3 on 2018-12-22 01:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20181220_2228'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloguser',
            old_name='last_verify',
            new_name='last_activity',
        ),
    ]
