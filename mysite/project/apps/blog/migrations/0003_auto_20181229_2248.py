# Generated by Django 2.1.3 on 2018-12-29 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20181223_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='status',
            field=models.CharField(blank=True, choices=[('P', 'POST'), ('A', 'ARTICLE')], default='P', max_length=12),
        ),
    ]