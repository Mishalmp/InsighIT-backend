from django.urls import path
from .views import *


urlpatterns=[

    path('text_generation/',ArticleContentcreationByOpenai.as_view(),name="text_generation")

]