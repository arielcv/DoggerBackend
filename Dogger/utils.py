from .models import User, DogOwner, Dog


def dogListByOwner(name):
    user = User.objects.get(username=name)
    owner = DogOwner.objects.get(user=user)
    dogs = Dog.objects.filter(owner=owner)
    return dogs
