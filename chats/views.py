from django.shortcuts import render
from .serializers import *
from rest_framework.generics import CreateAPIView,ListAPIView
# Create your views here.
from rest_framework.permissions import IsAuthenticated,AllowAny

class PrevoiusMessagesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=MessageSerializer

    def get_queryset(self):
        
        user1=int(self.kwargs['user1'])
        user2=int(self.kwargs['user2'])


        thread_suffix=f'{user1}_{user2}' if user1 > user2 else f'{user2}_{user1}'
        thread_name='chat_'+thread_suffix

        queryset=Message.objects.filter(
            thread_name=thread_name
        )

        return queryset
    
