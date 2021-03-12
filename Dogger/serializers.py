from rest_framework import serializers
from .models import Dog, DogOwner, DogWalker, User, Reservation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        validated_data['password'] = user.set_password(raw_password=validated_data['password'])
        user.save()
        return user


class DogWalkerSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='walker')
    user = UserSerializer()

    class Meta:
        model = DogWalker
        fields = ['email', 'user', 'role', 'name', 'bio', 'birthDate']

    def create(self, validated_data):
        validated_data.pop('role')
        user = validated_data.pop('user')
        userData = User.objects.create(username=user['username'],password= user['password'])
        userData.set_password(raw_password=user['password'])
        userData.save()
        return DogWalker.objects.create(**validated_data,user=userData)
    #
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()
    #     return instance

class DogSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    size = serializers.CharField()

    class Meta:
        model = Dog
        fields = '__all__'

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
    dogs = DogSerializer(many = True,read_only=True)

    class Meta:
        model = DogOwner
        fields = ['email', 'user', 'role', 'name', 'bio', 'birthDate','dogs']

    def create(self, validated_data):
        validated_data.pop('role')
        user = validated_data.pop('user')
        userData = User.objects.create(username=user['username'], password=user['password'])
        userData.set_password(raw_password=user['password'])
        userData.save()
        return DogOwner.objects.create(**validated_data, user=userData)

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['start','end','dog','walker','owner']

    def create(self, validated_data):
        return Reservation.objects.create(**validated_data)