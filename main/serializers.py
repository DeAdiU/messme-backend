from rest_framework import serializers
from .models import Orders, Mess, Menu, User

class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')  
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


class RegisterMessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mess
        fields = ('contact_no', 'password','name')  
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}