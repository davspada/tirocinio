from django.urls import path, include
from .views import (
    CameraList,
    DataListApiView,
    camera_frames,
    camera_frames_interval,
    create_video,
    get_all_videos,
    get_camera_videos,
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
    path('video_gallery', get_all_videos, name = 'video gallery'),
    path('video_gallery/<name>', get_camera_videos),
    path('<name>', camera_frames, name = 'camera frames'),
    path('<name>/<interval>', camera_frames_interval, name = 'camera frames interval'),
    path('<name>/<interval>/video', create_video)
]