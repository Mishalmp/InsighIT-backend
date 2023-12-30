from django.db import models

from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.
from celery import shared_task
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", 'admin')

        if extra_fields.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)






class User(AbstractUser):
    USER_TYPE=(
        ('user','user'),
        ('admin','Admin'),
    )
    

    first_name=models.CharField(max_length=200,null=True)
    last_name=models.CharField(max_length=200,null=True)
    username = models.CharField(max_length=150, unique=False)
    email=models.EmailField(max_length=250,unique=True)
    
    profile_img=models.ImageField(upload_to='user_profile_img/',blank=True,null=True)
    cover_img=models.ImageField(upload_to='user_cover_img/',blank=True,null=True)
    is_active=models.BooleanField(default=False)
    role=models.CharField(max_length=50,choices=USER_TYPE,default='user')
    is_google=models.BooleanField(default=False)
    is_completed=models.BooleanField(default=False)
    bio=models.TextField(max_length=500,null=True)
    tag_name=models.CharField(max_length=50,default='He/She')
    is_premium=models.BooleanField(default=False)
    wallet_balance=models.DecimalField(max_digits=20,decimal_places=2,default=0)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    objects=CustomUserManager()




class Followings(models.Model):
    follower=models.ForeignKey(User,related_name='following',on_delete=models.CASCADE)
    following=models.ForeignKey(User,related_name='followers',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=['follower','following']
    

    def __str__(self):

        return f'{self.follower.first_name} follows {self.following.first_name}'
    

        




class Skills(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    skill=models.CharField(max_length=100)
    rateofskills=models.IntegerField(default=0)


class PremiumUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='premiumuserinfo')
    
    subscription_price_basic = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    subscription_price_std = models.DecimalField(max_digits=10, decimal_places=2, default=75)
    sub_price_basic_yr = models.DecimalField(max_digits=10, decimal_places=2, default=250)
    sub_price_std_yr = models.DecimalField(max_digits=10, decimal_places=2, default=350)
    pan_number = models.CharField(max_length=10)
    bank_name=models.CharField(max_length=100,default='sbi')
    linkedin_url=models.CharField(max_length=100,default='skdcbkasbckaskcxbk')
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=20)
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.user.email



class Qualifications(models.Model):
    premium_user = models.ForeignKey(PremiumUserInfo, on_delete=models.CASCADE,related_name='qualifications')
    qualifications = models.CharField(max_length=100,null=True)

class Experiences(models.Model):
    premium_user = models.ForeignKey(PremiumUserInfo, on_delete=models.CASCADE,related_name='experiences')
    experience = models.CharField(max_length=200,null=True)


class PremiumRequests(models.Model):
    premium=models.ForeignKey(PremiumUserInfo,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_approved=models.BooleanField(default=False)



class Subscription(models.Model):
  
    SUBSCRIPTION_TYPE=[
        ('basic_monthly','Basic_monthly'),
        ('basic_yearly','Basic_yearly'),
        ('standard_monthly','Standard_monthly'),
        ('standard_yearly','Standard_yearly'),

    ]

    subscriber=models.ForeignKey(User,related_name='subscriptions',on_delete=models.CASCADE)
    subscribed_to=models.ForeignKey(User,related_name='subscribers',on_delete=models.CASCADE)
    subscription_type=models.CharField(max_length=30,choices=SUBSCRIPTION_TYPE)
    subscription_amount=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    is_active=models.BooleanField(default=False)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)

   
    def __str__(self):
        return f"{self.subscriber.first_name} subscribes to {self.subscribed_to.first_name} ({self.subscription_type}"



  


class Notifications(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    def __str__(self):

        return self.text


class Wallet(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    recieved_from=models.ForeignKey(User,related_name='recieved_transactions',on_delete=models.CASCADE)
    recieved=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    withdrawn=models.DecimalField(max_digits=20,decimal_places=2,default=0)
    created_at=models.DateTimeField(auto_now_add=True)



    # class Meta:
    #     unique_together=['user_id','recieved','created_at']

class Report_Issue(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    issue=models.TextField()
    is_fixed=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

