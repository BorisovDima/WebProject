# Generated by Django 2.1.3 on 2018-12-23 16:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_data', models.DateTimeField(default=django.utils.timezone.now)),
                ('text', models.TextField(max_length=424)),
                ('is_active', models.BooleanField(default=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent_comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
