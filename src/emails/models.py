from django.db import models
import uuid

from decouple import config

# Create your models here.
class Email(models.Model):
    active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class EmailVerificationEvent(models.Model):
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    email = models.EmailField()
    token = models.UUIDField(default=uuid.uuid4)
    expired = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_attempt_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    expired_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )

    def get_link(self):
        base_url = config("BASE_URL", cast=str)
        return f"{base_url}/verify/{self.token}/"