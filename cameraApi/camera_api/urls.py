from django.urls import path, include
from .views import (
    CameraList,
    DataListApiView,
    camera_frames,
    get_frames,
    post_frame,
    get_frame,
    index
)

urlpatterns = [
    #displays all data
    path('all', DataListApiView.as_view()),
    path('post_frame', post_frame.as_view()),
    path('get_camera_frames', get_frames.as_view()),
    path('get_camera_frame', get_frame.as_view()),
    path('home', index, name= 'index'),
    path('cameras_list', CameraList.as_view(), name = 'Cameras list'),
    path('<name>', camera_frames, name = 'name')
    #path('<name>/interval',)
]