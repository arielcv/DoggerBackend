from rest_framework import serializers
from .models import Dog, DogOwner, DogWalker, User, Reservation, WalkerConstraint
from .utils import createUser


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        validated_data['password'] = user.set_password(raw_password=validated_data['password'])
        user.save()
        return user


class DogWalkerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    role = serializers.CharField(default='walker')
    user = UserSerializer()

    class Meta:
        model = DogWalker
        fields = ['id', 'email', 'user', 'role', 'name', 'bio', 'birthDate']

    def create(self, validated_data):
        userData = createUser(validated_data)
        return DogWalker.objects.create(**validated_data, user=userData)

    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance


class DogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = ['id', 'name', 'size', 'owner']

    def create(self, validated_data):
        return Dog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.size = validated_data.get('size', instance.size)
        instance.save()
        return instance


class DogOwnerSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='owner')
    user = UserSerializer()
    dogs = DogSerializer(many=True, read_only=True)

    class Meta:
        model = DogOwner
        fields = ['id', 'email', 'user', 'role', 'name', 'bio', 'birthDate', 'dogs']

    def create(self, validated_data):
        userData = createUser(validated_data)
        return DogOwner.objects.create(**validated_data, user=userData)


class ReservationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    dog = DogSerializer(read_only=True)
    walker = DogWalkerSerializer(read_only=True)
    owner = DogOwnerSerializer(read_only=True)

    dogId = serializers.IntegerField(write_only=True, required=False)
    walkerId = serializers.IntegerField(write_only=True, required=False)
    ownerId = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Reservation
        fields = ['id', 'start', 'end', 'dog', 'walker', 'owner', 'dogId', 'walkerId', 'ownerId', 'confirmed']

    def create(self, validated_data):
        dogId = validated_data.pop('dogId')
        dog = Dog.objects.get(id=dogId)
        walkerId = validated_data.pop('walkerId')
        walker = DogWalker.objects.get(id=walkerId)
        ownerId = validated_data.pop('ownerId')
        owner = DogOwner.objects.get(id=ownerId)
        return Reservation.objects.create(**validated_data, dog=dog, walker=walker, owner=owner)

    def update(self, instance, validated_data):
        instance.confirmed = validated_data.get('confirmed', instance.confirmed)
        instance.save()
        return instance


class ConstraintSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    walkerId = serializers.IntegerField(write_only=True)

    class Meta:
        model = WalkerConstraint
        fields = ['id','walkerId','start','end','sizesAllowed']