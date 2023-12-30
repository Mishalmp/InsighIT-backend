from rest_framework import serializers
from accounts.models import *
from accounts.serializers import *
from blogs.models import *



class QualificationSerializers(serializers.ModelSerializer):
    
    class Meta:
        model=Qualifications
        fields='__all__'


class ExperiencesSerializers(serializers.ModelSerializer):
    class Meta:
        model=Experiences
        fields='__all__'



class PremiuminfoCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PremiumUserInfo
        fields = '__all__'


class PremiumInfoListSerializer(serializers.ModelSerializer):
    qualification = QualificationSerializers(source='qualifications', many=True, required=False)
    experience = ExperiencesSerializers(source='experiences', many=True, required=False)
    user=UserSerializer(read_only=True)
    class Meta:
        model = PremiumUserInfo
        fields = '__all__'



class PremiumRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=PremiumRequests
        fields='__all__'



class PremiumRequestSerializer(serializers.ModelSerializer):
    premium=PremiumInfoListSerializer()
    class Meta:
        model=PremiumRequests
        fields='__all__'
