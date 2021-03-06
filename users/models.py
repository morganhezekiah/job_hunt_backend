
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.db.models.signals import post_save


class UserManager(BaseUserManager):
    def create_user(self,email, password):
        if not email:
            raise ValueError("Please enter an email")

        if not password:
            raise ValueError("Please enter a password")

        
        email = self.normalize_email(email)
        user = self.model(email=email,password=make_password(password))
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(email, password)
        user.is_active=True
        user.is_super=True
        user.is_admin=True
        user.is_staff=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)
    phoneNumber = models.TextField(unique=False, null=True, blank=True)
    username = models.TextField(unique=True)
    slug = models.TextField(null=False, blank=False, unique=True)
    is_super = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_admin= models.BooleanField(default=False)
    is_staff= models.BooleanField(default=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD="email"
    PASSWORD_FIELD="password"
    REQUIRED_FIELDS = ['password']


    def has_perm(self, obj):
        return True

    def has_module_perms(self, obj):
        return True

    def equals(self,  object):
        return self.id == object.id
    
    object = UserManager()




class UserPaymentManager(models.Model):
    is_paid = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="payment")
    date_paid = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.email



def onUserCreated(instance, created, *args, **kwargs):
    if created:
        UserPaymentManager.objects.create(user= instance)



post_save.connect(onUserCreated, sender=User)



class Sponsor(models.Model):
    email = models.EmailField(null=False, blank=False)
    website = models.TextField(null=False, blank=False)
    joined_on = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.email