# Generated by Django 2.1.3 on 2019-01-05 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_info', models.CharField(choices=[('A', 'About'), ('PP', 'Privacy policy'), ('H', 'Help'), ('C', 'Contacts')], max_length=50, verbose_name='Type info')),
                ('text', models.TextField()),
            ],
        ),
    ]
