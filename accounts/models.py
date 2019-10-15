from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Counties(models.Model):
    county = models.CharField(max_length=100)

    def __str__(self):
        return self.county

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    #additional fields here
    is_sponsor = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    first_name = models.CharField(null=False, max_length=30)
    last_name = models.CharField(null=False, max_length=30)

    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    def __str__(self):
        return self.email



class Urban(models.Model):
    urban_centre = models.CharField(max_length=100, null=True)
    county = models.ForeignKey(Counties,on_delete=models.CASCADE)

    def __str__(self):
        return self.urban_centre

class Skills(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

# class Minor(models.Model):
#     skill = models.CharField(max_length=100)

#     def __str__(self):
#         return self.skill


class Creator(CustomUser):
    '''
    creating a profile model for each creator
    '''
    image = models.ImageField(upload_to='profile/', null= True, blank= True)
    stage_name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, blank = False)
    bio = models.TextField(max_length=500, blank= True)
    county = models.ForeignKey(Counties, on_delete = models.CASCADE, null= True, blank= True)
    urban_centre = models.ForeignKey(Urban ,on_delete=models.CASCADE, null= True, blank= True )
    major_skill = models.ForeignKey(Skills, on_delete=models.CASCADE, null= True, blank= True, related_name='major_skill' )
    minor_skill = models.ForeignKey(Skills, on_delete=models.CASCADE, null= True, blank= True, related_name='minor_skill' )
    agree_to_license = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta: 
        verbose_name = 'Creator'
        verbose_name_plural = 'Creators'


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Creator, through='Membership')

    def __str__(self):
        return self.name

class Membership(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.creator




