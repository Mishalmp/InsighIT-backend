from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView,ListAPIView,CreateAPIView

from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from rest_framework.response import Response
import traceback
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Count

# Create your views here.


class TopicsListCreateView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Topics.objects.filter(is_block = False)
    serializer_class=TopicsSerializer


    # def get_queryset(self):
        
    #     queryset=Topics.objects.filter(is_block = False).order_by('-id')

    #     sort = self.request.query_params.get('sort')
    #     if sort:
    #         if sort == 'popular':
    #             queryset = Topics.objects.filter(is_block=False).order_by('-num_blogs')
            
    #     return queryset



    # permission_classes=[IsAuthenticated]


    # def get(self, request, *args, **kwargs):
    #     topics = self.get_queryset()
    #     serializer = self.get_serializer(topics, many=True)
    #     return Response(serializer.data)




class TopicsView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Topics.objects.all()
    serializer_class=TopicsSerializer
    # permission_classes=[IsAuthenticated]


class MostUsedtopics(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=TopicsSerializer

    def get_queryset(self):
        return Topics.objects.filter(is_block=False).annotate(blog_count=Count('blogs')).order_by('-blog_count')[:4]



class CommunityCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset=Community.objects.all()
    serializer_class=CommunityCreateSerializer

class CommunityListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=CommunitySerializer
    queryset=Community.objects.all().order_by('-created_at')

class Communitydetailview(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=CommunitySerializer
    queryset=Community.objects.all()

class CommunityListByUser(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class=CommunitySerializer

    def get_queryset(self):
        
        return Community.objects.filter(user=self.kwargs.get('user_id')).order_by('-created_at')



class BlogsListCreateView(ListCreateAPIView):
    queryset = Blogs.objects.all()
    serializer_class = CreateSerializer
    permission_classes = (IsAuthenticated,)


    # def post(self, request, *args, **kwargs):
    #     try:
    #         # Assign the current user to the user_id field when creating a new blog
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save(user_id=request.user.id)

    #         return Response({'success': 'Blog created successfully'}, status=status.HTTP_201_CREATED)
    #     except Exception as e:

    #         print(traceback.format_exc())
    #         # Handle the exception and return an error response
    #         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from django.db.models import Q
class ListBlogsView(ListAPIView):
    
    permission_classes = (IsAuthenticated,)
    serializer_class=Blogserializer
    filter_backends = [SearchFilter]
    search_fields=['title','topic__topic','user_id__first_name']

    def get_queryset(self):
        
        topic=self.request.query_params.get('topic')
        sort = self.request.query_params.get('sort', 'latest')
        queryset = Blogs.objects.filter(is_block=False, is_hide=False)

        if topic:
            queryset = queryset.filter(topic__topic=topic)

        if sort == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort == 'popular':
            
            queryset = queryset.order_by('-likes')

        return queryset



class TrendingBlogsListView(ListAPIView):
    serializer_class = Blogserializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        trending_blogs = Blogs.objects.filter(is_block=False).order_by('-likes')[:5]
        return trending_blogs

class BlogDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Blogs.objects.all()
    serializer_class=Blogserializer
    permission_classes = (IsAuthenticated,)




class BlogsByUserListView(ListAPIView):
    serializer_class = Blogserializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [SearchFilter]
    search_fields = ['title', 'topic__topic']
    filterset_fields = ['user_id']

    def get_queryset(self):
        topic = self.request.query_params.get('topic')
        filter_value = self.request.query_params.get('filter')
        user_id = self.kwargs.get('user_id')

        queryset = Blogs.objects.filter(is_block=False, user_id=user_id).order_by('-created_at')

        if topic:
            queryset = queryset.filter(topic__topic=topic)

        if filter_value == 'visible':
            queryset = queryset.filter(is_hide=False)
        elif filter_value == 'hidden':
            queryset = queryset.filter(is_hide=True)

        return queryset
         

class CommentCreate(ListCreateAPIView):
    queryset=Comments.objects.all()
    serializer_class=CommentCreateSerializer
    permission_classes = (IsAuthenticated,)


class ListComments(ListAPIView):
    serializer_class=CommentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        blogid=self.kwargs.get('blog')
        queryset=Comments.objects.filter(blog=blogid).order_by('-created_at')

        return queryset


class CommentRetrieveDestroy(RetrieveUpdateDestroyAPIView):

    queryset=Comments.objects.all()
    serializer_class=CommentSerializer
    permission_classes = (IsAuthenticated,)

from django.db.models import F
class LikeCreateView(ListCreateAPIView):
    queryset=Like.objects.all()
    serializer_class=LikeCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        
        blog_id = request.data.get('blog')
        Blogs.objects.filter(id=blog_id).update(likes=F('likes') + 1)

        liked = True 
        return JsonResponse({'detail': 'Liked successfully.', 'liked': liked}, status=201)


class LikeView(RetrieveUpdateDestroyAPIView):
    serializer_class=LikeCreateSerializer
    queryset=Like.objects.all()
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        
        blog_id=request.data.get('blog')
        user_id=request.data.get('user')

        like=Like.objects.filter(blog=blog_id,user=user_id).first()

        if like:
            like.delete()
            Blogs.objects.filter(id=blog_id).update(likes=F('likes') - 1)
            liked = False  
            return JsonResponse({'detail': 'Unliked successfully.', 'liked': liked}, status=200)
        else:
            return JsonResponse({'detail': 'Like not found.'}, status=404)
   
        
    def get(self, request, *args, **kwargs):

        blog_id = request.GET.get('blog')
        user_id = request.GET.get('user')
        
       
        like=Like.objects.filter(blog=blog_id,user=user_id).exists()
       

        if like:
            liked=True
        else:
            liked=False
        print(liked,'likeeeeed')
        return JsonResponse({'detail': 'like fetched successfully.', 'liked': like}, status=200)


class ReportListCreate(ListCreateAPIView):
    queryset=Report_blog.objects.all()
    serializer_class=ReportBlogSerializer
    permission_classes = (IsAuthenticated,)

class ReportListView(ListAPIView):
    # queryset=Report_blog.objects.all()
    serializer_class=ReportListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset=Report_blog.objects.all().order_by('-reported_at')
        return queryset
        
class ReportBlogview(RetrieveUpdateDestroyAPIView):
    queryset=Report_blog.objects.all()
    serializer_class=ReportBlogSerializer
    permission_classes = (IsAuthenticated,)


class CreateSavedView(CreateAPIView):
    queryset=SavedBlogs.objects.all()
    serializer_class=SavedCreateSerializer
    permission_classes = (IsAuthenticated,)


class ListSavedbyUser(ListAPIView):
    serializer_class=SavedListSerializer
    filter_backends = [SearchFilter]
    search_fields=['title','topic__topic']
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        
        return SavedBlogs.objects.filter(user=self.kwargs['user_id']).order_by('-created_at')

class IsSavedView(RetrieveUpdateDestroyAPIView):
    serializer_class=SavedCreateSerializer
    queryset=SavedBlogs.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        user_id=request.GET.get('user_id')
        blog_id=request.GET.get('blog_id')

        Is_saved=SavedBlogs.objects.filter(user=user_id,blog=blog_id).exists()

        return Response({'detail':'saved checked successfully','saved':Is_saved},status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        
        user_id=request.GET.get('user_id')
        blog_id=request.GET.get('blog_id')


        Is_saved=SavedBlogs.objects.filter(user=user_id,blog=blog_id).first()

        if Is_saved:
            Is_saved.delete()

            return Response({'detail':'item deleted from saved',"saved":False},status=status.HTTP_301_MOVED_PERMANENTLY)
        else:
            return Response({'detail':"saved not found"},status=status.HTTP_404_NOT_FOUND)
