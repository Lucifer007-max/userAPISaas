from rest_framework import serializers
from api.models import  Cart, Login, Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Users.objects.create(**validated_data)
        return user
    



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'

    # def create(self, validated_data):
    #     login = Login.objects.create(**validated_data)
    #     return login
    

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    