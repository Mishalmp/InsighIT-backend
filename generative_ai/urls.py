from django.urls import path
from .views import *


urlpatterns=[

    path('text_generation/',ArticleContentcreationByOpenai.as_view(),name="text_generation"),
    path('get_technology_news/', get_technology_news, name='get_technology_news')

]