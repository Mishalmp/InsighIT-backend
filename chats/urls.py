from django.urls import path
from .views import *


urlpatterns=[
    path('user-previous-chats/<int:user1>/<int:user2>/',PrevoiusMessagesView.as_view())

]
