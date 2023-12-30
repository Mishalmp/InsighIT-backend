from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView
from accounts.models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
# Create your views here.
from rest_framework.filters import SearchFilter


class PremiumUserInfoListCreateView(ListCreateAPIView):
    queryset=PremiumUserInfo.objects.all()
    serializer_class=PremiuminfoCreateSerializer
    permission_classes = (IsAuthenticated,)


class PremiumInfoListView(ListAPIView):
    # queryset=PremiumUserInfo.objects.all()
    filter_backends=[SearchFilter]
    search_fields=['user__first_name','user__email']
    serializer_class=PremiumInfoListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        filter_value = self.request.query_params.get('filter')
        
        if filter_value == 'active':
        
            return PremiumUserInfo.objects.filter(is_approved = True).order_by('-created_at')
        elif filter_value == 'inactive':
            
            return PremiumUserInfo.objects.filter(is_approved = False).order_by('-created_at')
        else:
       
            return PremiumUserInfo.objects.all().order_by('-created_at')



class PremiumUserInfoDetailView(RetrieveUpdateDestroyAPIView):
    queryset=PremiumUserInfo.objects.all()
    serializer_class=PremiumInfoListSerializer
    permission_classes = (IsAuthenticated,)

class Premiuminfobyuser(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=PremiumInfoListSerializer
    lookup_field='user'

    def get_queryset(self):
        user_id=self.kwargs.get('user')
        premiumview=PremiumUserInfo.objects.filter(user=user_id)
        return premiumview
    

class Premiumrequestview(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=PremiumRequests.objects.all()
    serializer_class=PremiumRequestCreateSerializer

class PremiumrequestList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=PremiumRequests.objects.all()
    serializer_class=PremiumRequestSerializer

class PremiumrequestDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=PremiumRequests.objects.all()
    serializer_class=PremiumRequestSerializer



class ExperienceListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Experiences.objects.all()
    serializer_class=ExperiencesSerializers


class QualificationsListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Qualifications.objects.all()
    serializer_class=QualificationSerializers
