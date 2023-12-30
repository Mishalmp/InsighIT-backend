from django.db.models.signals import post_save,post_delete,pre_save
from django.dispatch import receiver

from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone
from .models import *
from blogs.models import *
from django.conf import settings
from .tasks import send_mail_user_block,send_mail_user_premium
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

channel_layer = get_channel_layer()


@receiver(post_save, sender=User)
def send_mail_user_block_signal(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active != instance._state.fields_cache.get('is_active', {}).get('original'):
            send_mail_user_block.delay(instance.email, instance.is_active)



@receiver(post_save, sender=User)
def send_mail_premium_status_signal(sender, instance, created, *args, **kwargs):
    if not created:
       
        if instance.is_premium != instance._state.fields_cache.get('is_premium', {}).get('original'):
            send_mail_user_premium.delay(instance.email,instance.is_premium)




@receiver(post_save,sender=User)
def send_user_created_notification(sender,instance,created,*args,**kwargs):

    if created:
        notification_text = f'New user is created {instance.first_name} {instance.last_name}'
        
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(user=admin_user,text=notification_text )

              
        async_to_sync(channel_layer.group_send)(
            "admin_group",
            {
                'type': 'create_notification',
                'message': notification_text
            }
        )



@receiver(post_save,sender=PremiumUserInfo)
def send_user_created_notification(sender,instance,created,*args,**kwargs):

    if created:
        notification_text = f'New premium user request has been recieved {instance.user.first_name} {instance.user.last_name}'
        
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(user=admin_user,text=notification_text )

              
        async_to_sync(channel_layer.group_send)(
            "admin_group",
            {
                'type': 'create_notification',
                'message': notification_text
            }
        )



@receiver(post_save, sender=Subscription)
def send_notification_subs(sender, instance, created, **kwargs):

    if created:
        notification_text = f'{instance.subscriber.first_name} {instance.subscriber.last_name} subscribed to {instance.subscribed_to.first_name} ({instance.subscription_type})'
        
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(user=admin_user,text=notification_text )




@receiver(post_delete, sender=Subscription)
def delete_related_followings(sender, instance, **kwargs):
    print('Deleting related followings...')
    print('Follower:', instance.subscriber)
    print('Following:', instance.subscribed_to)
    Followings.objects.filter(follower=instance.subscriber, following=instance.subscribed_to).delete()


@receiver(post_save, sender=Subscription)
def update_subscription_price(sender, instance, created, **kwargs):
    subscribed_to = instance.subscribed_to
    subscribers_count = Subscription.objects.filter(subscribed_to=subscribed_to).count()

    if subscribers_count % 10 == 0 and subscribed_to.is_premium:
        premium_info = subscribed_to.premiumuserinfo
        premium_info.subscription_price_basic += 10
        premium_info.subscription_price_std += 10
        premium_info.sub_price_basic_yr += 50
        premium_info.sub_price_std_yr += 50

        premium_info.save()

        notification_text = "Your subscription price has been increased by 10"
        Notifications.objects.create(user=subscribed_to, text=notification_text)


@receiver(post_save, sender=Wallet)
def send_notification_wallet(sender, instance, created, **kwargs):

    if created:
        notification_text = f'Amount has been recieved from {instance.recieved_from.first_name} {instance.recieved_from.last_name}'
        
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(user=admin_user,text=notification_text )

        # Send real-time notification
      
        async_to_sync(channel_layer.group_send)(
            "admin_group",
            {
                'type': 'create_notification',
                'message': notification_text
            }
        )



@receiver(post_save, sender=Report_Issue)
def send_notification_report(sender, instance, created, **kwargs):

    if created:
        notification_text = f'A new report has been recieved from {instance.user.first_name} {instance.user.last_name}'
        
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(user=admin_user,text=notification_text )

        # Send real-time notification
       
        async_to_sync(channel_layer.group_send)(
           "admin_group",
            {
                'type': 'create_notification',
                'message': notification_text
            }
        )

@receiver(post_save, sender=Blogs)
def create_blog_notification(sender, instance, created, **kwargs):
    if created:
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(
            user=admin_user,
            text=f'{instance.user.first_name} {instance.user.last_name} created a new blog: {instance.title}'
        )
        followers = Followings.objects.filter(following=instance.user)
        for follower in followers:
            Notifications.objects.create(
                user=follower.follower,
                text=f'{instance.user.first_name} {instance.user.last_name} created a new blog: {instance.title}'
            )

@receiver(post_save, sender=Community)
def create_community_notification(sender, instance, created, **kwargs):
    if created:
        admin_user = User.objects.filter(is_superuser = True).first()
        Notifications.objects.create(
            user=admin_user,
            text=f'{instance.user.first_name} {instance.user.last_name} created a new community post: {instance.text}'
        )
        followers = Followings.objects.filter(following=instance.user)
        for follower in followers:
            Notifications.objects.create(
                user=follower.follower,
                text=f'{instance.user.first_name} {instance.user.last_name} created a new community post: {instance.text}'
            )
            