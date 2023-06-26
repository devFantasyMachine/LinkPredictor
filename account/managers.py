from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    """
    Custom user model manager where email or phone is the unique identifier
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """
        :param username:
        :param password:
        :param extra_fields: other's fields
        :return: user
        :rtype: User
        """

        if not email or not password:
            raise ValueError(_("Users must have an email address"))

        email = BaseUserManager.normalize_email(email)
        now = timezone.now()

        user = self.model(email=email,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self._create_user(email, password, **extra_fields)
