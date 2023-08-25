from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Reply, News


@receiver(post_save, sender=Reply)
def notify_lot_owner(sender, instance, **kwargs):
    if kwargs['created']:
        lot = instance.reply_lots
        lot_owner = lot.lots_user.site_user
        subject = 'Новый отзыв на ваш лот'
        message = f'На ваш лот "{lot.title}" появился новый отзыв: {instance.text}'
        from_email = 'crypto.sch@yandex.ru'
        recipient_list = [lot_owner.email]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Reply)
def notify_reply_sender(sender, instance, **kwargs):
    if instance.status:
        reply_sender = instance.reply_user
        lot = instance.reply_lots
        subject = 'Ваш отзыв был принят'
        message = f'Ваш отзыв на лот "{lot.title}" был принят: {instance.text}'
        from_email = 'crypto.sch@yandex.ru'
        recipient_list = [reply_sender.email]

        send_mail(subject, message, from_email, recipient_list)
