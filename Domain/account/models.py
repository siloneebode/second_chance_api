from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.text import slugify


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **kwargs):

        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email.')
        if password is None:
            raise TypeError('User must have an email.')
        user = self.model(username=username,
                          email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.user_slug = slugify(username)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **kwargs):
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(update_fields=('is_superuser', 'is_staff'))
        return user


class User(AbstractBaseUser, PermissionsMixin):
    LANGUAGES = (
        ('FR', 'Français'),
        ('EN', 'Anglais'),
        ('YE', 'Yemba'),
        ('GO', 'Ghomala\'a'),
        ('EWO', 'Ewondo'),
        ('FU', 'Fulfulde'),
        ('DU', 'Duala'),
    )
    uid = models.CharField(default=None, null=True, max_length=255)
    email = models.EmailField(unique=True, null=False, max_length=255)
    username = models.CharField(null=False, max_length=255, db_index=True)
    password = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    first_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    email_confirmed = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    banned_at = models.DateTimeField(null=True)
    age = models.DateTimeField(null=True)
    bio = models.TextField(max_length=500, null=True)
    last_login_ip = models.GenericIPAddressField(null=True)
    user_slug = models.SlugField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    total_sold = models.IntegerField(default=0)
    total_cancel = models.IntegerField(default=0)
    total_complete = models.IntegerField(default=0)
    cancel_rate = models.FloatField(default='0')
    delivery_rate = models.FloatField(default='0')
    user_rate = models.FloatField(default='0')
    lang = models.CharField(default='FR', choices=LANGUAGES, max_length=50)
    new_follower = models.BooleanField(default=True)
    new_order = models.BooleanField(default=True)
    new_offer = models.BooleanField(default=True)
    new_favorite = models.BooleanField(default=True)
    new_evaluation = models.BooleanField(default=True)
    banned_level = models.IntegerField(null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def can_login(self):
        return self.banned_at is None


class Group(models.Model):
    name = models.CharField(null=False, max_length=255)
    owners = models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

# group = Group().owners.add(User())
