from django.shortcuts import render
from .models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import HttpResponseRedirect
# Create your views here.


from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny


from decouple import config

site_url = config('SITE_URL')

print(site_url)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class=MyTokenObtainPairSerializer



class UserRegister(CreateAPIView):
    permission_classes=(AllowAny,)

    def get_serializer_class(self):
        return UserSerializer

    def post(self,request):

        email=request.data.get('email')
        password=request.data.get('password')
       

        serializer=UserSerializer(data=request.data)
        
       

        if serializer.is_valid(raise_exception=True):

            user=serializer.save()
            user.set_password(password)
            user.save()
            
            
            current_site=get_current_site(request)
            mail_subject='please activate your account'
            messsage=render_to_string('user/account_verification.html',
            {

                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user)

            })
            to_email=email
            send_mail=EmailMessage(mail_subject,messsage,to=[to_email])
            send_mail.send()

            return Response({'status':'success','msg':'a verification link send to your email','data':serializer.data,})
        else:
            return Response({'status':'error','msg':serializer.errors})


          
@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()  # Decode the bytes to a string
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        message = "Congratulations, Successfully registered"

        redirect_url = site_url+'/login/' + '?message=' + message + '&token=' + token  
    else:
        message = 'Invalid activation Link'
        redirect_url = site_url+'/signup/' + '?message=' + message

    return HttpResponseRedirect(redirect_url)



class GoogleUser(APIView):
    permission_classes=(AllowAny,)
    def post(self,request):
        email=request.data.get('email')
        password=request.data.get('password')


        if not User.objects.filter(email=email).exists():
            serializer=UserGoogleSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                user=serializer.save()
                user.role='user'
                user.is_active=True
                user.is_google=True
                user.set_password(password)
                user.save()

        user=authenticate(request,email=email,password=password)

        if user is not None:

            token=create_jwt_pair_tokens(user)

            response_data={
                "status":"success",
                "token":token,
                "msg":"account has been registered Successfully"
            }

            return Response(data=response_data,status=status.HTTP_201_CREATED)
        else:
            return Response(data={'status':'400','msg':'login Failed'})


@permission_classes([AllowAny])
def create_jwt_pair_tokens(user):

    refresh=RefreshToken.for_user(user)

    refresh['email']=user.email
    refresh['id']=user.id
    refresh['first_name']=user.first_name
    refresh['last_name']=user.last_name
    refresh['role']=user.role
    refresh['is_active']=user.is_active

    access_token=str(refresh.access_token)
    refresh_token=str(refresh)

    return{
        "access_token":access_token,
        "refresh_token":refresh_token
    }



# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])

class ForgotPassword(APIView):
    permission_classes=(AllowAny,)
    def post(self,request):
        email=request.data.get('email')


        if User.objects.filter(email=email).exists():
            user=User.objects.get(email__exact=email)
            current_site=get_current_site(request)
            mail_subject='Click this link to change password'
            message=render_to_string('user/forgotpassword.html',
            {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
                'site':current_site


            })

            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()

            return Response(
                data={
                    'message':"verification email has been sent to your email address",
                    'user_id':user.id,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                data={'message':"No Account found"},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([AllowAny])
def reset_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        return HttpResponseRedirect(f'{site_url}/resetpassword/')  

class ResetPassword(APIView):
    permission_classes=(AllowAny,)
    def post(self,request,format=None):
        str_user_id=request.data.get('user_id')
        # print(str_user_id,"111111111")
        uid=int(str_user_id)
        password=request.data.get('password')

        if uid:
            user=User.objects.get(id=uid)
            user.set_password(password)
            user.save()
            return Response(data={'message':'password reset successfully'},status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class UpdateUser(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=User.objects.all()
    serializer_class=UserInfoSerializer


class ChangePassword(APIView):

    permission_classes = (IsAuthenticated,)
    def put(self,request):

        old_password = request.data.get('current_password')
        new_password = request.data.get("new_password")
        user_id=request.data.get('user_id')

        user = User.objects.get(id=user_id)

        if not user.check_password(old_password):
            return Response({'error':'Invalid old password'},status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()

        return Response({'message':"Password changed successfully"},status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            # print(refresh_token,'reeeeeeeeeeeeeffffffffffffreeeeeeeeeeeeeeeeeee')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
