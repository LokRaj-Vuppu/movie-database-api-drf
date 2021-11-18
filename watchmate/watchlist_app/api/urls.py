from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import movie_list, movie_details
from .views import (ReviewDetails, ReviewCreate, UserReviews, WatchDetailsAV, 
                    WatchListAV,
                     ReviewList, StreamPlatformViewSet, WatchListGV)


router = DefaultRouter()
router.register('stream', StreamPlatformViewSet, basename='streamplatform')


urlpatterns = [
    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>', WatchDetailsAV.as_view(), name='movie-details'),
    path('list2/', WatchListGV.as_view(), name='movie-list2'),

    path('', include(router.urls)),
    
    # path('stream/list/', StreamPlatformListAV.as_view(), name='stream_platform-list'),
    # path('stream/<int:pk>/', StreamPlatformDetailAV.as_view(), name='stream_platform-details'),
    
    # path('reviews', ReviewList.as_view() , name='review-list'),
    # path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'),

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review_list'),
    path('reviews/<int:pk>/', ReviewDetails.as_view(), name='review-details'),


    path('user-reviews/', UserReviews.as_view(), name='review-search'),
]