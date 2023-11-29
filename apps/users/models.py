from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password.strip())

        user.save()
        return user

    def create_superuser(self,email, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff = True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        return self.create_user(email, password=password, **extra_fields)


class Vendor(AbstractBaseUser):

    email = models.EmailField(_('email'), max_length=255, unique=True, db_index=True)
    username = models.CharField(_('username'), max_length=300, blank=True, null=True, db_index=True)
    phone_number = models.CharField(_("Phone_Number"), max_length=50, blank=True, null=True, db_index=True)
    password = models.CharField(_('password'), max_length=100, blank=True, null=True)
    address = models.TextField(_('address'), max_length=255, unique=True, editable=False, blank=True, null=True)
    vendor_code = models.CharField(_('vendor_code'), blank=True, null=True,max_length=255)
    on_time_delivery_rate = models.FloatField(_('on_time_delivery_rate'), blank=True, null=True)
    quality_rating_avg = models.FloatField(_('quality_rating_avg'), blank=True, null=True)
    average_response_time = models.FloatField(_('average_response_time'), blank=True, null=True)
    fulfillment_rate = models.FloatField(_('fulfillment_rate'), blank=True, null=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Is Active'), default=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return "{username}".format(username=self.username)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True