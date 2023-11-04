# serializer.py
from rest_framework import serializers
from .models import CustomUser, Company
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            raise serializers.ValidationError("User field cannot be updated.")
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create(**user_data)
        validated_data['user'] = user
        custom_user = CustomUser.objects.create(**validated_data)
        custom_user.company.no_of_employees += 1
        custom_user.company.save()
        return custom_user


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'
