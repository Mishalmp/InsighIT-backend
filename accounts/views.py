from datetime import datetime
from django.shortcuts import render,redirect
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,CreateAPIView,ListAPIView,DestroyAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django.http import JsonResponse
from django.middleware.csrf import get_token
from decimal import Decimal
from django.db.models import Sum,Q,Count, F, Q
from dashboard.serializers import *

from django.db.models.functions import Coalesce

stripe.api_key=settings.STRIPE_SECRET_KEY

endpoint_secret = settings.STRIPE_SECRET_WEBHOOK



class SingleUserInfo(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=User.objects.all()
    serializer_class=UserInfoSerializer


class CreateSkills(ListCreateAPIView):
    queryset=Skills.objects.all()
    serializer_class = SkillSerializer
    permission_classes = (IsAuthenticated,)

class ListSkills(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=SkillSerializer
    

    def get_queryset(self):
        user_id=self.kwargs.get('user_id')
        queryset=Skills.objects.filter(user_id=user_id)

        return queryset



class SkillView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Skills.objects.all()
    serializer_class=SkillSerializer


class NotificationsListCreate(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Notifications.objects.all()
    serializer_class=NotificationSerializer

class Notificationbyuser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=NotificationSerializer

    def get_queryset(self):
        user_id=self.kwargs.get('user_id')
        queryset=Notifications.objects.filter(user=user_id,is_read=False).order_by('-created_at')

        return queryset
    

class ClearAllNotifications(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=NotificationSerializer
    lookup_field = 'user_id'
    def get_queryset(self):
        user_id = self.kwargs.get('user_id')

        return Notifications.objects.filter(user=user_id, is_read=False)
    
    def delete(self, request, *args, **kwargs):
        
        queryset = self.get_queryset()
        queryset.update(is_read=True)

        return Response({'message': 'All notifications cleared successfully.'}, status=status.HTTP_204_NO_CONTENT)
        
    
class TrendingUsers(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
       
        premium_users = User.objects.filter(is_premium=True).annotate(
            followers_count=Coalesce(Count('followers'), 0),
            followings_count=Coalesce(Count('following'), 0),
        ).order_by('-followers_count')[:4]

        # Serialize the data
        serializer = UserInfoSerializer(premium_users, many=True)

       
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class SubscriptionList(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Subscription.objects.all()
    serializer_class=SubscriptionSerializer

    def perform_create(self, serializer):
        subscription_amount=serializer.validated_data['subscription_amount']

        recieved_amount=Decimal('0.6') * subscription_amount
        subscription=serializer.save()

        subscribed_to_user=subscription.subscribed_to
        subscribed_to_user.wallet_balance += recieved_amount
        subscribed_to_user.save()


        subscribed_to_wallet=Wallet.objects.create(user_id=subscription.subscribed_to,recieved=recieved_amount,recieved_from=subscription.subscriber)
       
        subscribed_to_wallet.save()

        admin_user=User.objects.get(role='admin')
        admin_user.wallet_balance += subscription_amount - recieved_amount
        admin_user.save()

        admin_wallet=Wallet.objects.create(
            user_id=admin_user,
            recieved=subscription_amount-recieved_amount,
            recieved_from=subscription.subscriber
        )
       

        admin_wallet.save()
    
    def create(self, request, *args, **kwargs):
        
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers=self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)




class SubscriptionListByUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=SubscriptionlistSerializer
    
    def get_queryset(self):
        return Subscription.objects.filter(subscriber=self.kwargs['user_id'])
         
class SubscribersListByUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=SubscriptionlistSerializer

    def get_queryset(self):
        return Subscription.objects.filter(subscribed_to=self.kwargs['user_id'])


class IsSubscriber(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,user_id,blog_author, *args, **kwargs):
       
        try:
            is_subscriber=Subscription.objects.filter(subscriber=user_id,subscribed_to=blog_author,is_active=True).exists()

            return Response({"is_subscriber":is_subscriber},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e) }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Is_standard_subscriber(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request,user_id,author_id, *args, **kwargs):

        try:
            is_standard_subscriber = Subscription.objects.filter(
                subscriber=user_id,
                subscribed_to=author_id,
                subscription_type__in=['standard_monthly', 'standard_yearly'],
                is_active=True
            ).exists()

            return Response({'is_standard_subscriber':is_standard_subscriber},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class FollowingsCreate(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Followings.objects.all()
    serializer_class=FollowingsSerializers


class Unfollow(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Followings.objects.all()
    serializer_class=FollowingsSerializers

    def destroy(self, request, *args, **kwargs):
        try:
           
            following_inst=Followings.objects.get(follower=self.kwargs['follower_id'],following=self.kwargs['following_id'])
            self.perform_destroy(following_inst)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Followings.DoesNotExist:
            return Response({"error":"Following not found"},status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Isfollowing(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request,follower_id,following_id,*args,**kwargs):
        try:
            is_follower=Followings.objects.filter(follower=follower_id,following=following_id).exists()

            return Response({'is_follower':is_follower},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FollowingsList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=FollowinglistSerializer
    
    def get_queryset(self):
        user_id=self.kwargs['user_id']
        return Followings.objects.filter(follower=user_id)

class FollowersList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=FollowinglistSerializer

    def get_queryset(self):
        
        user_id=self.kwargs['user_id']
        return Followings.objects.filter(following=user_id)


from chats.models import Message
from django.db.models import Max, F

class ChatUsersList(ListAPIView):
    serializer_class=FollowinglistSerializer
    permission_classes = (IsAuthenticated,)

    def get(self,request,user_id):
        followings=Followings.objects.filter(follower=user_id)
        followers=Followings.objects.filter(following=user_id)

        users=list(followings.values_list('following', flat=True)) + list(followers.values_list('follower', flat=True))

        chat_users=User.objects.filter(pk__in=users)

        serializers=UserSerializer(chat_users,many=True)
        
        return Response({'chat_users': serializers.data})



class ListWallet(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=Walletserializer
    
    def get_queryset(self):
        
        return Wallet.objects.filter(user_id=self.kwargs['user_id'])
    
    def list(self, request, *args, **kwargs):
        
        queryset=self.get_queryset()

        aggregated_data=queryset.aggregate(
            total_recieved=Sum('recieved'),
            total_withdrawn=Sum('withdrawn')
        )


        serializer=self.get_serializer(queryset,many=True)

        
        response_data={
          
            'transactions':serializer.data,
            'total_recieved':aggregated_data['total_recieved'] or 0,
            'total_withdrawn':aggregated_data['total_withdrawn'] or 0,
        }

        return Response(response_data)


class ReportIssueCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=ReportIssueCreateSerializer
    queryset=Report_Issue.objects.all()

class ReportIssueListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=ReportIssueSerializer
    queryset=Report_Issue.objects.all().order_by('-created_at')

class ReportissueDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=ReportIssueSerializer
    queryset=Report_Issue.objects.all()
        
        
        

class ReportIssuesbyUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=ReportIssueSerializer

    def get_queryset(self):
        
        return Report_Issue.objects.filter(user=self.kwargs.get('user_id')).order_by('-created_at')
    

class PremiumUserList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=UserListSerializer
    queryset=User.objects.filter(is_active=True,is_premium=True).order_by('-id')



#----------------payment STRIPE------------------------------

# @method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):

        author=self.request.data['author_id']
        pre_author=User.objects.get(id=author)

      
        try:
            # subscription_data = {
            #     'subscriber': self.request.data['user_id'],
            #     'subscribed_to': self.request.data['author_id'],
            #     'subscription_type':self.request.data['subscription_type'],  
            #     'is_active': True,
            # }

            checkout_session=stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data':{
                        'currency':'INR',
                        'unit_amount':int(self.request.data['price'])*100,
                        'product_data':{
                            'name':pre_author.first_name+' '+pre_author.last_name,
                            'images':[
                                pre_author.profile_img.url,
                                # 'https://www.searchenginejournal.com/wp-content/uploads/2020/03/the-top-10-most-popular-online-payment-solutions-5e9978d564973.png'
                            ],
                        }
                        },
                        'quantity':1,
                        # 'payment_method_types': ['upi'],

                    },
                ],
                mode='payment',
            
                success_url = f"{self.request.data['origin_site']}?success=true&subscriber={self.request.data['user_id']}&subscribed_to={self.request.data['author_id']}&subscription_type={self.request.data['subscription_type']}&subscription_amount={self.request.data['subscription_amount']}"
,
                cancel_url=self.request.data['origin_site']+'?cancel=true'
            )

            

            # print('333333',checkout_session)
            return Response({ "message" : checkout_session },status= status.HTTP_200_OK)


        except Exception as e:
            return Response({ "message" : str(e)},status= status.HTTP_500_INTERNAL_SERVER_ERROR)

# @csrf_exempt
# def stripe_webhook_view(request):
#     payload = request.body
#     sig_header = request.headers.get('Stripe-Signature')

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, endpoint_secret
#         )
#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     # Handle the event
#     if event['type'] == 'payment_intent.succeeded':
#         print('successs')
#         # Do something

#     return HttpResponse(status=200)

     



         
