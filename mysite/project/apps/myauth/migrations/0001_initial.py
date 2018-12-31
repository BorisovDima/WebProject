# Generated by Django 2.1.3 on 2018-12-27 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BanList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ban', models.BooleanField(default=False)),
                ('attempts', models.IntegerField(default=0)),
                ('time_unblock', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.GenericIPAddressField()),
            ],
        ),
    ]