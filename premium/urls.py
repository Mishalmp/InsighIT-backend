from django.urls import path
from .views import *

urlpatterns=[
    path('premiumuserinfo/',PremiumUserInfoListCreateView.as_view(),name='premium-user-create'),
    path('premiumuserinfolist/',PremiumInfoListView.as_view(),name='premium-list'),
    path('premiumuserinfoview/<int:pk>/',PremiumUserInfoDetailView.as_view(),name='premiuminfo-view'),
    path('premiumuserinfouserview/<int:user>/',Premiuminfobyuser.as_view(),name='premiuminfo-view'),
    path('premiumrequestcreate/',Premiumrequestview.as_view(),name='premium-req-create'),
    path('premiumuserrequestlist/',PremiumrequestList.as_view(),name='premium-req-list'),
    path('premiumuserreqview/<int:pk>/',PremiumrequestDetailView.as_view(),name='premium-req-view'),

    path('experiences/',ExperienceListCreateView.as_view(),name='experience-view'),
    path('qualifications/',QualificationsListCreateView.as_view(),name='qualifications-view'),

]

