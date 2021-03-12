from django.contrib import admin
from .models import DogOwner, DogWalker, Dog, User, TimeStamp, Reservation

# Register your models here.
admin.site.register(Dog)
admin.site.register(DogOwner)
admin.site.register(DogWalker)
admin.site.register(User)
admin.site.register(TimeStamp)
admin.site.register(Reservation)