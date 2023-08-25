import self as self
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from django.core.mail import send_mail



class SiteUser(models.Model):
    site_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_user = models.IntegerField(default=0)
    email = models.EmailField(null=True, blank=True, default=None)

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


    def get_absolute_url(self):
        return reverse('lots_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'lots-{self.pk}')


class Reply(models.Model):
    reply_lots = models.ForeignKey('Lots', on_delete=models.CASCADE)
    reply_user = models.OneToOneField(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=256)
    status = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.status:
            notify_lot_owner(sender=Reply, instance=self)



class News(models.Model):
    author = models.ForeignKey('SiteUser', on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=256, null=True, blank=True, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        subject = 'Новая новость'
        message = f'Появилась новая новость: {self.title}'
        from_email = 'crypto.sch@yandex.ru'
        recipient_list = SiteUser.objects.values_list('email', flat=True)

        send_mail(subject, message, from_email, recipient_list)
