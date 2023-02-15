from django.db import models
# from django.contrib.auth import get_user_model # avoid using
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
# User = get_user_model()

class User(AbstractUser): #preferred
    #cellphone_number=models.CharField(max_length=15)
    is_organisor=models.BooleanField(default=True)
    is_agent=models.BooleanField(default=False)

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username

# Create your models here.
class Lead(models.Model):
    # SOURCE_CHOICES=(
    #     ("YouTube","YouTube")
    #     ("Google","Google")
    #     ("Newsletter","Newsletter")
    #     )
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    age=models.IntegerField(default=0)
    organization=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    agent=models.ForeignKey("Agent",null=True,blank=True,on_delete=models.SET_NULL)
    category=models.ForeignKey("Category",related_name="leads",on_delete=models.SET_NULL,null=True,blank=True)
    
    # phoned=models.BooleanField(default=False,null=False)
    # source=models.CharField(choices=SOURCE_CHOICES,max_length=100)

    # profile_picture=models.ImageField(blank=True,null=True)
    # special_files=models.FileField(blank=True,null=True)
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Agent(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    organization= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username

class Category(models.Model):
    name=models.CharField(max_length=30) #New,Contacted,Unconverted,Converted
    organization= models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.name

def post_user_created_signal(sender, instance, created, **kwargs):
    #print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal,sender=User)