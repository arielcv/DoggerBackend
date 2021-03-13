from rest_framework.parsers import JSONParser
from .models import User, DogOwner, Dog

def dogListByOwner(name):
    user = User.objects.get(username=name)
    owner = DogOwner.objects.get(user=user)
    dogs = Dog.objects.filter(owner=owner)
    return dogs


def createUser(validated_data):
    validated_data.pop('role')
    user = validated_data.pop('user')
    userData = User.objects.create(username=user['username'], password=user['password'])
    userData.set_password(raw_password=user['password'])
    userData.save()
    return userData

def signUser(request):
    data = JSONParser().parse(request)
    user = {'username': data['name'], 'password': data['password']}
    userDict = dict()
    userDict['email'] = data.pop('email')
    userDict['user'] = user
    return userDict