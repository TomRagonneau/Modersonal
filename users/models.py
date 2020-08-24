import re

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import TblUserManager

# Quick-start model field settings
TITLES = ((0, _('Prof.')), (1, _('Dr.')), (2, _('Mr.')), (3, _('Ms.')), (4, _('Mrs.')))
FIRST_NAME_MAX_LENGTH = getattr(settings, 'USER_FIRST_NAME_MAX_LEN', 50)
LAST_NAME_MAX_LENGTH = getattr(settings, 'USER_LAST_NAME_MAX_LEN', 50)


class TblUser(AbstractBaseUser, PermissionsMixin):
    """TBL User model."""

    email = models.EmailField(_('email address'), unique=True)
    title = models.IntegerField(choices=TITLES, default=0)
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title', 'first_name', 'last_name']

    objects = TblUserManager()

    def save(self, *args, **kwargs):
        # Before being dumped into the database, the users fields first_name and
        # last_name are pretreated:
        # 1. All the excessive blank characters are removed.
        # 2. All the spaces are stripped.
        # 3. The cases of each field are titled.
        self.first_name = re.sub('\s\s+', ' ', self.first_name.strip().title())
        self.last_name = re.sub('\s\s+', ' ', self.last_name.strip().title())
        super(TblUser, self).save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(
            next(title[1] for title in TITLES if title[0] == self.title),
            self.last_name
        )
