from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.core.validators import MinLengthValidator

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)

class Major(models.Model):
    skill = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.skill

class Minor(models.Model):
    skill = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.skill

class Counties(models.Model):
    county = models.CharField(max_length=100)

    def __str__(self):
        return self.county

class Urban(models.Model):
    urban_centre = models.CharField(max_length=100, null=True)
    county = models.ForeignKey(Counties, null=True)

    def __str__(self):
        return self.urban_centre

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    stage_name = models.CharField(max_length=5)
    phone = models.CharField(max_length=12, blank=False, null=True, validators=[MinLengthValidator(10)])
    county = models.ForeignKey(Counties, null=True)
    urban_centre = models.ForeignKey(Urban, null=True)
    major_skill = models.ForeignKey(Major, null=True)
    minor_skill = models.ForeignKey(Minor, null=True)
    photo = models.ImageField(upload_to='uploads', blank=True)


