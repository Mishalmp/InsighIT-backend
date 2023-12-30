from django.urls import path
from .views import *

urlpatterns = [
    path('topics/', TopicsListCreateView.as_view(), name='topics-list-create'),
    path('trendingtopics/', MostUsedtopics.as_view(), name='trending-topics'),
    path('topicsview/<int:pk>/',TopicsView.as_view(),name='topic-view'),
    path('blogs/', BlogsListCreateView.as_view(), name='blogs-list-create'),
    path('blogdetail/<int:pk>/', BlogDetailView.as_view(), name='blogs-detail'),
    path('blogslist/',ListBlogsView.as_view(),name='blogs-list'),
    path('trendingblogs/',TrendingBlogsListView.as_view(),name='trendingblogs'),

    path('communitycreate/',CommunityCreateView.as_view(),name='communities-create'),
    path('communitylist/',CommunityListView.as_view(),name='communities-list'),
    path('communityview/<int:pk>/',Communitydetailview.as_view(),name='communities-view'),
    path('communitiesbyuser/<int:user_id>/',CommunityListByUser.as_view(),name='communitieslist-by-user'),



   

    path('blogs/by-user/<int:user_id>/', BlogsByUserListView.as_view(), name='blogs-by-user'),
    path('commentslistcreate/',CommentCreate.as_view(),name='comments-list-create'),
    path('commentslist/<int:blog>/',ListComments.as_view(),name='comments-list'),
    path('comment-retrieve-destroy/<int:pk>/',CommentRetrieveDestroy.as_view(),name='comment-retrieve-destroy'),
    path('likes/',LikeCreateView.as_view(),name='like-blog'),
    path('likeview/',LikeView.as_view(),name='unlike-blog'),
    path('reportblogs/',ReportListCreate.as_view(),name='reportblogs'),
    path('reportbloglist/',ReportListView.as_view(),name='reportslist'),
    path('reportview/<int:pk>/',ReportBlogview.as_view(),name='reportview'),
    path('createsaved/',CreateSavedView.as_view(),name='createsaved'),
    path('listsaved/<int:user_id>/',ListSavedbyUser.as_view(),name='listsaved'),
    path('saveview/',IsSavedView.as_view(),name='saveview'),
    
]   