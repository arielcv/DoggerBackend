from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True,unique=True)
    password = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.name

class DogOwner(models.Model):
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.id)

class Dog(models.Model):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = "large"

    CATEGORIES = ((SMALL,'Small'),
                  (MEDIUM,'Medium'),
                  (LARGE,'Large'))

    name = models.CharField(max_length=50)
    size = models.CharField(max_length=50,choices=CATEGORIES)
    owner = models.ForeignKey(DogOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class DogWalker(models.Model):
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    schedule = {}

    def __str__(self):
        return self.user.username

