from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    #additional fields here
    is_sponsor = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)

    def __str__(self):
        return self.email


# class Role(models.Model):
#   '''
#   The Role entries are managed by the system,
#   automatically created via a Django data migration.
#   '''
#   CONSUMER = 1
#   CREATOR = 2
#   SPONSOR = 3
#   ADMIN = 4
#   ROLE_CHOICES = (
#       (CONSUMER, 'consumer'),
#       (CREATOR, 'creator'),
#       (SPONSOR, 'sponsor'),
#       (ADMIN, 'admin'),
#   )

#   id = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, primary_key=True)

#   def __str__(self):
#       return self.get_id_display()