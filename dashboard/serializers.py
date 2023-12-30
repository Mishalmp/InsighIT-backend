from rest_framework import serializers
from rest_framework_simplejwt.tokens import Token
from accounts.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import ValidationError
from rest_framework.serializers import ModelSerializer



class AdminTokenObtainPairSerializers(TokenObtainPairSerializer):

    @classmethod

    def get_token(cls,user):
        token=super().get_token(user)

        if not user.is_active:
            raise ValidationError("User is not active",code='inactive user')
       

        token['user_id']=user.id
        token['role']=user.role
        token['email']=user.email
        token['is_active']=user.is_active
        token['is_superuser']=user.is_superuser

        return token

class UserListSerializer(ModelSerializer):
    class Meta:
        model=User
        exclude=('password',)

class BlockUnblockSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=['is_active']

