from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Dog, DogOwner, DogWalker, User, TimeStamp, Reservation, WalkerConstraint
from .serializers import DogSerializer, DogOwnerSerializer, DogWalkerSerializer, UserSerializer, ReservationSerializer, \
    ConstraintSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
import datetime
import pytz
from .utils import signUser, parseDateTime

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
    userDict = signUser(request)
    dogOwnerSerializer = DogOwnerSerializer(data=userDict)
    if dogOwnerSerializer.is_valid():
        dogOwnerSerializer.save()
        return Response(dogOwnerSerializer.data, status=status.HTTP_201_CREATED)
    return Response(dogOwnerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def dogList(request):
    if request.method == 'GET':
        dogs = Dog.objects.all()
        serializer = DogSerializer(dogs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        owner = data.pop('owner')
        try:
            owner = DogOwner.objects.get(name=owner['name'])
            data['owner'] = owner.id
            print(data)
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
    userDict = signUser(request)
    dogWalkerSerializer = DogWalkerSerializer(data=userDict)
    if dogWalkerSerializer.is_valid():
        dogWalkerSerializer.save()
        return Response(dogWalkerSerializer.data, status=status.HTTP_201_CREATED)
    return Response(dogWalkerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def dogOwnerDetails(request, name):
    try:
        ownerUser = User.objects.get(username=name)
        dogOwner = DogOwner.objects.get(user=ownerUser)
        dogs = Dog.objects.filter(owner=dogOwner)
        serializer = DogOwnerSerializer(dogOwner, dogs=dogs)
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


@api_view(['GET'])
def dogOwnerReservation(request, name):
    try:
        ownerUser = User.objects.get(username=name)
        dogOwner = DogOwner.objects.get(user=ownerUser)
        reservations = Reservation.objects.filter(owner=dogOwner).all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogOwner.DoesNotExist:
        return Response("The specified user is not an owner", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
def dogWalkerReservation(request, name):
    try:
        walkerUser = User.objects.get(username=name)
        dogWalker = DogWalker.objects.get(user=walkerUser)
        if request.method == 'GET':
            reservationsAssigned = Reservation.objects.filter(walker=dogWalker).all()
            reservationsUnassigned = Reservation.objects.filter(walker=None).all()
            serializerAssigned = ReservationSerializer(reservationsAssigned, many=True)
            serializerUnassigned = ReservationSerializer(reservationsUnassigned, many=True)
            return Response([serializerAssigned.data,serializerUnassigned.data])
        elif request.method == 'POST':
            data = (JSONParser().parse(request))
            dogWalker.schedule = list(TimeStamp.objects.filter(walker=dogWalker).order_by('dt'))
            dog = data.pop('dog')
            dog = Dog.objects.get(id=dog)
            owner = dog.owner
            (startDatetime, endDatetime) = parseDateTime(data)
            startTimeStamp = TimeStamp(walker=dogWalker, dt=startDatetime)
            endTimeStamp = TimeStamp(walker=dogWalker, dt=endDatetime)
            update = dogWalker.assign(startTimeStamp, endTimeStamp, dog.size)
            data['dogId'] = dog.id
            data['walkerId'] = dogWalker.id
            data['ownerId'] = owner.id
            constraints = WalkerConstraint.objects.filter(walker=dogWalker,
                                                          sizesAllowed__in=[dog.size, 'all'],
                                                          start__lte=datetime.time(hour=startDatetime.hour,
                                                                                   minute=startDatetime.minute),
                                                          end__gte=datetime.time(hour=endDatetime.hour,
                                                                                 minute=endDatetime.minute))
            if constraints:
                serializer = ReservationSerializer(data=data)
                if update and serializer.is_valid():
                    for dt in update:
                        dt.save()
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Error", status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return Response('There are no times available for your reservation', status=status.HTTP_403_FORBIDDEN)
        elif request.method == 'PATCH':
            data = (JSONParser().parse(request))
            reservation = Reservation.objects.filter(walker=dogWalker).filter(id=data['id'])[0]
            serializer = ReservationSerializer(reservation, data={'confirmed': True}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        elif request.method == 'DELETE':
            data = (JSONParser().parse(request))
            reservation = Reservation.objects.filter(walker=dogWalker).filter(id=data['id'])[0]
            start = reservation.start
            end = reservation.end
            reservationInterval = TimeStamp.objects.filter(dt__gte=start - datetime.timedelta(minutes=1)).filter(
                dt__lte=end + datetime.timedelta(minutes=1))
            for r in reservationInterval:
                r.decreaseBoth()
                r.delete() if r.isNull() else r.save()
                reservation.delete()

    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogWalker.DoesNotExist:
        return Response("The specified user is not a walker", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def dogWalkerConstraintsList(request, name):
    try:
        dogWalker = DogWalker.objects.get(name=name)
        if request.method == 'GET':
            constraints = list(WalkerConstraint.objects.filter(walker=dogWalker))
            serializer = ConstraintSerializer(constraints, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            print(data['start'])
            (startDatetime, endDatetime) = parseDateTime(data)
            data['start'] = datetime.time(hour=startDatetime.hour, minute=startDatetime.minute,
                                          second=startDatetime.second)
            data['end'] = datetime.time(hour=endDatetime.hour, minute=endDatetime.minute,
                                          second=endDatetime.second)
            data['walkerId'] = dogWalker.id
            sizes = data.pop('sizesAllowed')
            serializerList =[]
            for size in sizes:
                data['sizesAllowed'] = size
                serializer = ConstraintSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    serializerList.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = ConstraintSerializer(serializerList, many=True)
                return Response(response.data,status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogWalker.DoesNotExist:
        return Response("The specified user is not a walker", status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
def dogWalkerConstraintsDetails(request, id):
    try:
        constraint = WalkerConstraint.objects.get(id=id)
        if request.method == 'GET':
            serializer = ConstraintSerializer(constraint)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            constraint.delete()
            return Response('Deletion Completed', status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response("The user does not exist", status=status.HTTP_404_NOT_FOUND)
    except DogWalker.DoesNotExist:
        return Response("The specified user is not a walker", status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def acceptReservation(request,id):
    try:
        data = JSONParser().parse(request)
        reservation = Reservation.objects.get(id = id)
        walker = DogWalker.objects.get(name=data['walker'])
        reservation.walker = walker
        reservation.confirmed = True
        reservation.save()
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data,status=status.HTTP_200_OK)
    except Reservation.DoesNotExist:
        return Response('Error',status=status.HTTP_404_BAD_REQUEST)
    except DogWalker.DoesNotExist:
        return Response('Error',status=status.HTTP_404_BAD_REQUEST)