# Generated by Django 4.2.4 on 2023-08-25 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='time_creation',
        ),
        migrations.AddField(
            model_name='news',
            name='author',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='market.siteuser'),
        ),
        migrations.AddField(
            model_name='news',
            name='title',
            field=models.CharField(blank=True, default=None, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='reply',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='siteuser',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='reply_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
