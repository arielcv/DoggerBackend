from django.contrib.auth.models import AbstractUser, User
from django.db import models

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, blank=True, null=True,unique=True)
    password = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.name


class DogOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name = self.user.username if self.name == '' else self.name
        super(DogOwner, self).save()

    def __str__(self):
        return str(self.name)


class Dog(models.Model):
    SMALL = 'small'
    MEDIUM = 'medium'
    LARGE = "large"

    CATEGORIES = ((SMALL,'Small'),
                  (MEDIUM,'Medium'),
                  (LARGE,'Large'))

    name = models.CharField(max_length=50, unique=True)
    size = models.CharField(max_length=50,choices=CATEGORIES)
    owner = models.ForeignKey(DogOwner, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class DogWalker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    schedule = {}

    def save(self, *args, **kwargs):
        self.name = self.user.username if self.name == '' else self.name
        super(DogWalker, self).save()

    def __str__(self):
        return self.name

