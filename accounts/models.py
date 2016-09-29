from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Group
from django.db import models
from django.db.models.signals import post_save

from notifications.signals import notify


class MyUserManager(BaseUserManager):
    def create_user(self, username=None, email=None, password=None):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not username:
            raise ValueError('Username Field must be included')

        if not email:
            raise ValueError('Users must have a valid email address')

        #if not gender:
            #raise ValueError('Gender must be included')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given username, email and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            #gender=gender,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    #gender = models.ChoiceField()
    is_member = models.BooleanField(default=False, verbose_name='Premium User')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    #is_superuser = models.BooleanField(default=False) -- upgrades to be done later

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" %(self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __unicode__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class UserProfile(models.Model):
    """docstring for UserProfile"""
    user = models.OneToOneField(MyUser)
    biography = models.TextField(null=True, blank=True)
    facebook_connect = models.CharField(max_length=400, null=True, blank=True, verbose_name='facebook link url')
    twitter_handle = models.CharField(max_length=400, null=True, blank=True, verbose_name='twitter handle')


    def __unicode__(self):
        return self.user.username


def new_user_signal_reciever(sender, instance, created, *args, **kwargs):
    if created:
        new_profile, is_created = UserProfile.objects.get_or_create(user=instance)
        print new_profile, is_created
        notify.send(
            instance,
            recipient=MyUser.objects.get(username="mathemartins"),
            verb = 'a new user just joined primenerds',
        )

post_save.connect(new_user_signal_reciever, sender=MyUser)
