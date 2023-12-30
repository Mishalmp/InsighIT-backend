from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.models import User
from .models import Message
from accounts.serializers import UserSerializer


class MessageSerializer(ModelSerializer):
    sender_email=serializers.EmailField(source='sender.email')

    class Meta:
        model=Message
        fields=['message','sender_email','timestamp']





