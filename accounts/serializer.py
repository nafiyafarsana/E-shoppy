from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegister(serializers.ModelSerializer):

    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model=User
        fields=['username','email','password', 'confirm_password'] 
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def save(self):
        reg=User(
            email = self.validated_data['email'],
            username = self.validated_data['username']
        )
        password=self.validated_data['password']
        confirm_password = self.validated_data['confirm_password']
        
        if password != confirm_password:
            raise serializers.ValidationError({'password':'Passwords must match'})
        reg.set_password(password)
        reg.save()
        return reg



class UserUpdateSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type':'password'},write_only=True, required=False)
    password = serializers.CharField(style={'input_type':'password'},write_only=True, required=False)

    class Meta:
        model=User
        fields=['username','email', 'password', 'confirm_password'] 
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        password = validated_data.get('password')
        confirm_password = validated_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError({'password': 'password does not match'})
        if password:
            instance.set_password(password)
        instance.save()

        return instance
