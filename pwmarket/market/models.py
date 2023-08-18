from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse


class SiteUser(models.Model):
    site_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)

    def update_rating(self):
        pass


class Lots(models.Model):
    lots_user = models.ForeignKey("SiteUser", on_delete=models.CASCADE)

    CHARACTER = 'CR'
    MONEY = 'MN'
    THINGS = 'TN'
    SERVICES = 'SV'

    CATEGORY_CHOICES = (
        (CHARACTER, 'Персонаж'),
        (MONEY, 'Юани'),
        (THINGS, 'Предметы'),
        (SERVICES, 'Услуги')
    )
    category_choice = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    time_creation = models.DateTimeField(auto_created=True)
    title = models.CharField(max_length=24)
    description = models.TextField()
    price = models.FloatField(default=0.0)

    # screenshot =

    def get_absolute_url(self):
        return reverse('lots_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'lots-{self.pk}')


class Reply(models.Model):
    reply_lots = models.ForeignKey('Lots', on_delete=models.CASCADE)
    reply_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    time_creation = models.DateTimeField(auto_now_add=True)


class News(models.Model):
    pass
