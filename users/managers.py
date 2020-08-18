from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class TblUserManager(BaseUserManager):
    """Management of TBL Users."""

    # Serialize the manager into migrations to have them available in RunPython operations.
    use_in_migrations = True

    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        kwargs.setdefault('is_superuser', False)

        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **kwargs)
