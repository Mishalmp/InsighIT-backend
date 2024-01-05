from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views_accounts import *
from .views import *

urlpatterns=[
    path('token/',MyTokenObtainPairView.as_view(),name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/',UserRegister.as_view(),name='register'),
    path('premiumlist/',PremiumUserList.as_view(),name="premiumlist"),
    path('activate/<uidb64>/<token>',activate, name='activate'),
    path('GoogleUser/',GoogleUser.as_view(), name='GoogleUser'),
    path('userinfo/<int:pk>/',SingleUserInfo.as_view(),name='userinfo'),
    path('trendingUsers/',TrendingUsers.as_view(),name='TrendingUsers'),


    path('forgotpassword/',ForgotPassword.as_view(),name='forgotpassword'),
    path('reset-validate/<uidb64>/<token>',reset_validate,name='reset_validate'),
    path('reset-passsword/',ResetPassword.as_view(),name='reset-password'),
    path('updateuser/<int:pk>/',UpdateUser.as_view(),name='updateuser'),
    path('changePassword/',ChangePassword.as_view(),name='changePassword'),

    path('skills/',CreateSkills.as_view(),name='skill-create'),
    path('skillview/<int:pk>/',SkillView.as_view(),name='skill-view'),
    path('listskills/<int:user_id>/',ListSkills.as_view(),name='list-skills'),

    path('notifications/',NotificationsListCreate.as_view(),name="notifications"),
    path('listnotification/<int:user_id>/',Notificationbyuser.as_view(),name='notificationbyuser'),
    path('clearallnotifications/<int:user_id>/',ClearAllNotifications.as_view(),name='clear_all_notifications'),

    path('subscriptions/',SubscriptionList.as_view(),name='subscriptions'),
    path('isSubscriber/<int:user_id>/<int:blog_author>/',IsSubscriber.as_view(),name='IsSubscriber'),
    path('isstandardSubscriber/<int:user_id>/<int:author_id>/',Is_standard_subscriber.as_view(),name='IsstandardSubscriber'),

    path('followingscreate/',FollowingsCreate.as_view(),name='followingcreate'),
    path('is_follower/<int:follower_id>/<int:following_id>/',Isfollowing.as_view(),name='is_follower'),
    path('unfollow/<int:follower_id>/<int:following_id>/',Unfollow.as_view(),name='unfollow'),

    path('followings/<int:user_id>/',FollowingsList.as_view(),name='follwings'),
    path('followers/<int:user_id>/',FollowersList.as_view(),name='followers'),
    path('chatusers/<int:user_id>/',ChatUsersList.as_view(),name='chat-users'),
   

    path('subscriptionslist/<int:user_id>/',SubscriptionListByUser.as_view(),name='subscriptions'),
    path('subscriberslist/<int:user_id>/',SubscribersListByUser.as_view(),name='subscribers'),
    path('wallet/<int:user_id>/',ListWallet.as_view(),name='wallet'),

    path('reportissuecreate/',ReportIssueCreateView.as_view(),name='reportcreate'),
    path('issuelist/',ReportIssueListView.as_view(),name='reportissuelist'),
    path('issuelistbyuser/<int:user_id>',ReportIssuesbyUser.as_view(),name='reportissuelistbyuser'),
    path('issueview/<int:pk>',ReportissueDetailView.as_view(),name='reportissuelistbyuser'),

    path('create-checkout-session/',CreateCheckoutSessionView.as_view(),name='checkout-session'),
    
    # path('webhook/stripe/',stripe_webhook_view,name='web_hook'),

]

