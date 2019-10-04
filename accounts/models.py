from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Counties(models.Model):
    county = models.CharField(max_length=100)

    def __str__(self):
        return self.county

class CustomUser(AbstractUser):
    #additional fields here
    is_sponsor = models.BooleanField(default=False)
    is_creator = models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.email



class Urban(models.Model):
    urban_centre = models.CharField(max_length=100, null=True)
    county = models.ForeignKey(Counties,on_delete=models.CASCADE)

    def __str__(self):
        return self.urban_centre

class Major(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill

class Minor(models.Model):
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill


class Creator(CustomUser):
    '''
    creating a profile model for each creator
    '''
    image = models.ImageField(upload_to='profile/', null= True)
    stage_name = models.CharField(max_length=100, null=True)
    Phone = models.CharField(max_length=10, blank = False)
    bio = models.TextField(max_length=500)
    county = models.ForeignKey(Counties, on_delete = models.CASCADE, blank = False)
    urban_centre = models.ForeignKey(Urban ,on_delete=models.CASCADE, blank = False )
    major_skill = models.ForeignKey(Major, on_delete=models.CASCADE, blank = False )
    minor_skill = models.ForeignKey(Minor, on_delete=models.CASCADE, blank = False )

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
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

    def __str__(self):
        return self.creator.first_name



