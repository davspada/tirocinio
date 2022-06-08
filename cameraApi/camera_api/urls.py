from django.urls import path, include
from .views import (
    DataListApiView,
    get_frames,
    post_frame,
    get_frame
)

urlpatterns = [
    #displays all data
    path('all', DataListApiView.as_view()),
    path('post_frame', post_frame.as_view()),
    path('get_camera_frames', get_frames.as_view()),
    path('get_camera_frame', get_frame.as_view())
]