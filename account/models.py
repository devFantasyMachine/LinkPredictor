import uuid

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

from account.managers import UserManager


def upload_to(instance, filename):
    return 'userImage/{filename}'.format(filename=filename)


class User(AbstractUser):
    """
     The User class : this class is used to represent a user of the gospelConnect application
    """
    objects = UserManager()

    username = models.CharField(max_length=150, blank=True, default="predictor")

    email = models.EmailField(_("email address"), unique=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    image = models.ImageField(_("Image of user"), upload_to=upload_to, default='userImage/default.jpg')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return "id: {} email: {}".format(self.id, self.email)
