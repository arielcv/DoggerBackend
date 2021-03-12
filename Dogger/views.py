from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Dog, DogOwner, DogWalker, User, TimeStamp, Reservation
from .serializers import DogSerializer, DogOwnerSerializer, DogWalkerSerializer, UserSerializer, ReservationSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import datetime
from dateutil.tz import tzlocal
import pytz

utc = pytz.UTC


# Create your views here.
@api_view(['GET'])
def dogOwnerList(request):
    owners = DogOwner.objects.all()
    serializer = DogOwnerSerializer(owners, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def dogOwnerSignUp(request):
    data = JSONParser().parse(request)
    print(data)
    user = {'username': data['name'], 'password': data['password']}
    print(user)
    userSerializer = UserSerializer(data=user)
    if userSerializer.is_valid():
        userSerializer.save()
        dogOwner = dict()
        dogOwner['email'] = data.pop('email')
        dogOwner['user'] = User.objects.get(username=data['name']).id
        print(dogOwner)
        dogOwnerSerializer = DogOwnerSerializer(data=dogOwner)
        if dogOwnerSerializer.is_valid():
            dogOwnerSerializer.save()
            return Response(dogOwnerSerializer.data, status=status.HTTP_201_CREATED)
        print('Dog Owner Error')
        return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    print('Person Error')
    return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def dogList(request):
    if request.method == 'GET':
        dogs = Dog.objects.all()
        serializer = DogSerializer(dogs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        ownerName = data['owner']
        try:
            user = User.objects.get(username=ownerName)
            owner = DogOwner.objects.get(user=user)
            data['owner'] = owner.id
            print(owner)
            dogSerializer = DogSerializer(data=data)
            if dogSerializer.is_valid():
                dogSerializer.save()
                return Response(dogSerializer.data, status=status.HTTP_201_CREATED)
            return Response(dogSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("The user does not exist", status=status.HTTP_400_BAD_REQUEST)
        except DogOwner.DoesNotExist:
            return Response("The specified user is not an owner", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def dogListByOwner(request, name):
    try:
        user = User.objects.get(username=name)
        owner = DogOwner.objects.get(user=user)
        dogs = Dog.objects.filter(owner=owner)
        serializer = DogSerializer(dogs, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_400_BAD_REQUEST)
    except DogOwner.DoesNotExist:
        return Response("The specified user is not an owner", status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dogWalkerList(request):
    walkers = DogWalker.objects.all()
    serializer = DogWalkerSerializer(walkers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def dogWalkerSignUp(request):
    data = JSONParser().parse(request)
    print(data)
    user = {'username': data['name'], 'password': data['password']}
    print(user)
    userSerializer = UserSerializer(data=user)
    if userSerializer.is_valid():
        userSerializer.save()
        dogWalker = dict()
        dogWalker['email'] = data.pop('email')
        dogWalker['user'] = User.objects.get(username=data['name']).id
        dogWalkerSerializer = DogWalkerSerializer(data=dogWalker)
        if dogWalkerSerializer.is_valid():
            dogWalkerSerializer.save()
            return Response(userSerializer.data, status=status.HTTP_201_CREATED)
        return Response(dogWalkerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def dogOwnerDetails(request, name):
    try:
        ownerUser = User.objects.get(username=name)
        dogOwner = DogOwner.objects.get(user=ownerUser)
        serializer = DogOwnerSerializer(dogOwner)
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogOwner.DoesNotExist:
        return Response("The specified user is not an owner", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
def dogDetails(request, id):
    try:
        dog = Dog.objects.get(id=id)
        if request.method == "GET":
            serializer = DogSerializer(dog)
            return Response(serializer.data)
        elif request.method == "POST":
            data = JSONParser().parse(request)
            data['owner'] = dog.owner.id
            serializer = DogSerializer(dog, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        elif request.method == "DELETE":
            dog.delete()
            return Response("The dog was removed", status=status.HTTP_200_OK)
    except Dog.DoesNotExist:
        return Response("There is no dog with that name", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getUser(request, name):
    try:
        user = User.objects.get(username=name)
        (role, roleType) = getRole(user)
        print(role)
        if roleType == 'owner':
            serializer = DogOwnerSerializer(role)
        elif roleType == 'walker':
            serializer = DogWalkerSerializer(role)
        else:
            print("Unexpected error")
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)


def getRole(user):
    ownersFiltered = DogOwner.objects.all().filter(user=user)
    walkersFiltered = DogWalker.objects.all().filter(user=user)
    if ownersFiltered:
        return (ownersFiltered[0], 'owner')
    elif walkersFiltered:
        return (walkersFiltered[0], 'walker')
    else:
        return (None, None)


@api_view(['GET'])
def dogWalkerDetails(request, name):
    try:
        walkerUser = User.objects.get(username=name)
        dogWalker = DogWalker.objects.get(user=walkerUser)
        serializer = DogWalkerSerializer(dogWalker)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogWalker.DoesNotExist:
        return Response("The specified user is not an walker", status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def dogWalkerReservation(request, id):
    try:
        walkerUser = User.objects.get(id=id)
        dogWalker = DogWalker.objects.get(user=walkerUser)
        dogWalker.schedule = list(TimeStamp.objects.filter(walker=dogWalker).order_by('dt'))
        data = (JSONParser().parse(request))
        parsedStart = ':'.join(data['start'].split(':')[0:2])
        parsedEnd = ':'.join(data['end'].split(':')[0:2])
        startTimeStamp = utc.localize(datetime.datetime.strptime(parsedStart, '%Y-%m-%dT%H:%M'))
        endTimeStamp = utc.localize(datetime.datetime.strptime(parsedEnd, '%Y-%m-%dT%H:%M'))
        startTimeStamp = TimeStamp(walker=dogWalker, dt=startTimeStamp)
        endTimeStamp = TimeStamp(walker=dogWalker, dt=endTimeStamp)
        update = dogWalker.assign(startTimeStamp, endTimeStamp)
        serializer = ReservationSerializer(data={'start':startTimeStamp.dt,'end':endTimeStamp.dt})
        if update and serializer.is_valid():
            for dt in update:
                dt.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response("Error", status=status.HTTP_406_NOT_ACCEPTABLE)
    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogWalker.DoesNotExist:
        return Response("The specified user is not an walker", status=status.HTTP_404_NOT_FOUND)
