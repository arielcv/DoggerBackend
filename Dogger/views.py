from django.http import HttpResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .models import Dog, DogOwner, DogWalker, User
from .serializers import DogSerializer, DogOwnerSerializer, DogWalkerSerializer, UserSerializer
from rest_framework.decorators import api_view


# Create your views here.
@api_view(['GET', 'POST'])
def dogOwnerList(request):
    if request.method == 'GET':
        owners = DogOwner.objects.all()
        serializer = DogOwnerSerializer(owners, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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
            return Response(dogOwnerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


@api_view(['GET', 'POST'])
def dogWalkerList(request):
    if request.method == 'GET':
        walkers = DogWalker.objects.all()
        serializer = DogWalkerSerializer(walkers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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
            print(dogWalker)
            # dogOwner['user'] = userSerializer
            dogWalkerSerializer = DogWalkerSerializer(data=dogWalker)
            if dogWalkerSerializer.is_valid():
                dogWalkerSerializer.save()
                return Response(dogWalkerSerializer.data, status=status.HTTP_201_CREATED)
            print('Dog Owner Error')
            return Response(dogWalkerSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print('Person Error')
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


@api_view(['GET','POST','DELETE'])
def dogDetails(request, name):
    try:
        dog = Dog.objects.get(name=name)

        if request.method == "GET":
            serializer = DogSerializer(dog)
            return Response(serializer.data)
        elif request.method == "POST":
            data = JSONParser().parse(request)
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

# user = {'name':data['name'],'email':data['email'], 'password':data['password']}
# dogOwner = {'name':data['name'],'email':data['email']}
# print(data)
# print(dogOwner)
#
# userSerializer = UserSerializer(data=user)
# print(userSerializer.is_valid())
# if True:
#     userObject = User.objects.create_user(user['name'],user['email'],user['password'])
#     dogOwner['user'] = userObject.id
#     serializer = DogOwnerSerializer(data=dogOwner)
#
#     if serializer.is_valid():
#         userSerializer.save()
#         serializer.save()
#         return JSONResponse(serializer.data, status=201)
#
# return JSONResponse(serializer.errors, status=400)

# def dogOwnerDetail(request, pk):
#     try:
#         dogOwner = DogOwner.objects.get(id=pk)
#     except DogOwner.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = DogSerializer(dogOwner)
#         return JSONResponse(serializer.data)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = DogOwnerSerializer(dogOwner, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         dogOwner.delete()
#         return HttpResponse(status=204)
#
#
# def dogList(request):
#     if request.method == "GET":
#         dogs = Dog.objects.all()
#         serializer = DogSerializer(dogs, many=True)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = DogOwnerSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#
#         return JSONResponse(serializer.errors, status=400)
#
#
# def dogDetail(request, pk):
#     try:
#         dog = Dog.objects.get(id=pk)
#     except Dog.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = DogSerializer(dog)
#         return JSONResponse(serializer.data)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = DogSerializer(dog, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         dog.delete()
#         return HttpResponse(status=204)
#
#
# def dogWalkerList(request):
#     if request.method == "GET":
#         dogs = DogWalker.objects.all()
#         serializer = Dog(dogs, many=True)
#         return JSONResponse(serializer.data)
#
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = DogWalkerSerializer(data=data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data, status=201)
#
#         return JSONResponse(serializer.errors, status=400)
#
#
# def dogWalkerDetail(request, pk):
#     try:
#         dogWalker = DogWalker.objects.get(id=pk)
#     except Dog.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = DogWalkerSerializer(dogWalker)
#         return JSONResponse(serializer.data)
#
#     elif request.method == "POST":
#         data = JSONParser().parse(request)
#         serializer = DogWalkerSerializer(dogWalker, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JSONResponse(serializer.data)
#         return JSONResponse(serializer.errors, status=400)
#
#     elif request.method == "DELETE":
#         dogWalker.delete()
#         return HttpResponse(status=204)

# @api_view(['GET'])
# def current_User(request):
#     serializer = DogOwnerSerializer
#     return Response(serializer.data)
