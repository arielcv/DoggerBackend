from rest_framework import serializers
from .models import Dog, DogOwner, DogWalker, User

class DogWalkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogWalker
        fields = ['email', 'user']

    def create(self, validated_data):
        return DogWalker.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        print(validated_data)
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('name', instance.email)
        instance.save()
        return instance


class DogOwnerSerializer(serializers.ModelSerializer):


    class Meta:
        model = DogOwner
        fields = ['email', 'user']


class DogSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    size = serializers.CharField()
    owner = DogOwner()

    class Meta:
        model = Dog
        fields = '__all__'

    def create(self, validated_data):
        return Dog.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     print(instance)
    #     print(validated_data)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.size = validated_data.get('size', instance.size)
    #     instance.owner = validated_data.get('owner', instance.owner)
    #     instance.save()
    #     return instance