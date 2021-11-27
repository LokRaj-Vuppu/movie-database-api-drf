from rest_framework import pagination, serializers, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.decorators import api_view
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from django_filters import rest_framework as filters
from rest_framework import filters
from watchlist_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCursorPagination
from watchlist_app.api.permissions import AdminorReadOnly, ReviewUserorReadOnly
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.models import WatchList, StreamPlatform, Review
from watchlist_app.api.throttling import StreamPlatformThrottle

import logging

# logger = logging.getLogger('django')


logger = logging.getLogger('django')
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')

# file_handler = logging.FileHandler('logs/sample.log')
# file_handler.setLevel(logging.ERROR)
# file_handler.setFormatter(formatter)

# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

# logger.addHandler(file_handler)
# logger.addHandler(stream_handler)

# Class based views

class WatchListGV(generics.ListAPIView):
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    pagination_class = WatchListCursorPagination
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['created']
    # ordering = ['number_rating']



class UserReviews(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        # username = self.kwargs['username']
        username = self.request.query_params.get('username')

        return Review.objects.filter(review_user__username=username)


class StreamPlatformViewSet(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAuthenticated]
    # throttle_classes = [StreamPlatformThrottle]
    throttle_scope = 'streaming'


# class StreamPlatformVS(viewsets.ViewSet):

#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        watchlist = WatchList.objects.get(pk=pk)

        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have reviewed already')

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating']) / 2
        
        watchlist.number_rating = watchlist.number_rating+ 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)



class ReviewList(generics.ListCreateAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    # filterset_fields = ('review_user__username', 'active')
    search_fields = ['review_user__username', 'description']


    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)



class ReviewDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewUserorReadOnly]



# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)



# class ReviewList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):

#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)



class WatchListAV(APIView):

    def get(self, request):
        movies = WatchList.objects.all()
        serializer = WatchListSerializer(movies, many=True)
        logger.debug(serializer.data)
        return Response(serializer.data)


    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors)


class WatchDetailsAV(APIView):

    def get(self, request, pk):
        
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            content = {'error': 'Movie not found'}
            logger.error(content)
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movie)
        logger.info('All watchlist names')
        logger.info(serializer.data)
        return Response(serializer.data)


    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(serializer.data)
            return Response(serializer.data)
        else:
            logger.error(serializer.errors)
            return Response(serializer.errors)


    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        content ={ 'response': 'deleted successfully' }
        return Response(content, status=status.HTTP_204_NO_CONTENT)



# class StreamPlatformListAV(APIView):

#     def get(self, request):
#         stream_platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(stream_platforms, many=True)
#         return Response(serializer.data)


#     def post(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)



# class StreamPlatformDetailAV(APIView):

#     def get(self, request, pk):
        
#         try:
#             stream_platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             content = {'error': 'Movie not found'}
#             return Response(content, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = StreamPlatformSerializer(stream_platform)
#         return Response(serializer.data)

    
#     def put(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(stream_platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

    
#     def delete(self, request, pk):
#         stream_platform = StreamPlatform.objects.get(pk=pk)
#         stream_platform.delete()
#         content ={ 'response': 'deleted successfully' }
#         return Response(content, status=status.HTTP_204_NO_CONTENT)



# For adding the data and fetching all the data
# Function based views
# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     elif request.method == 'POST':
#         serializer = MovieSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors)

# # For retrieving the single data, update and delete 

# @api_view(['GET', 'PUT', 'DELETE'])
# def movie_details(request, pk):

#     try:
#         movie = Movie.objects.get(pk=pk)
#     except Movie.DoesNotExist:
#         content = {'error': 'Movie not found'}
#         return Response(content, status=status.HTTP_404_NOT_FOUND)


#     if request.method == 'GET':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     elif request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         content ={ 'response': 'deleted successfully' }
#         return Response(content, status=status.HTTP_204_NO_CONTENT)
