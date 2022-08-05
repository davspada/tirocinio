from datetime import timedelta,datetime
from importlib.resources import path
import json
import os
import django
from django.http import HttpResponse
from django.shortcuts import redirect, render
from numpy import integer
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Data, Video
from .serializers import DataSerializer
from .forms import *
from itertools import chain
from django.core.files.storage import default_storage
from django.views import generic
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
import ffmpeg
from django.core.paginator import *

class DataListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the Data items for given requested user
        '''
        all_data = Data.objects.all() #.filter(user = request.user.id)
        serializer = DataSerializer(all_data, many=True)
        #print("test")
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        '''
        Create the Data with given Data data
        '''
        data = {
            'frame': request.data.get('frame'), 
            'position': request.data.get('position'), 
            'timestamp': request.data.get('timestamp'),
            'name' : request.data.get('name')
        }
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        Datas = Data.objects.all().delete()
        return Response('success')

class post_frame(APIView):
    
    
    def post(self, request, *args, **kwargs):

        form = DataForm(request.POST, request.FILES)
    
        if form.is_valid():
            form.save()
            serializer = DataSerializer(data=request.data)
            #print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            form = DataForm()
        return render(request, 'data_form.html', {'form' : form})
    
    
    def success(request):
        return HttpResponse('successfully uploaded')

class get_frames(APIView):

    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        reqname = request.data.get('name')
        data1 = request.data.get('ts1')
        data2 = request.data.get('ts2')
        requested_data = Data.objects.all().filter(name = reqname, timestamp__gte = data1, timestamp__lte=data2 ).order_by('timestamp')
        print(requested_data)
        serializer = DataSerializer(requested_data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        reqname = request.data.get('name')
        #data1 = request.data.get('ts1')
        data2 = request.data.get('ts2')
        requested_data = Data.objects.all().filter(name = reqname, timestamp__lte=data2 )

        serializer = DataSerializer(requested_data, many=True)
        print(serializer.data)
        requested_data.delete()
        return Response("deleted successfully", status=status.HTTP_200_OK)

class get_frame(APIView):

    permission_classes=[permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        reqname = request.data.get('name')
        data1 = datetime.strptime(request.data.get('ts1'),"%Y/%m/%d %H:%M:%S")
        data2 = datetime.strptime(request.data.get('ts2'),"%Y/%m/%d %H:%M:%S")
        print(data1, data2)
        lista=[]
        #requested_data = Data.objects.all().filter(name = reqname, timestamp__gte = data1, timestamp__lte=data2 ).order_by('timestamp').iterator()
        while data1 < data2:
            data1.strftime("%m/%d/%Y-%H:%M:%-S")
            data2.strftime("%m/%d/%Y-%H:%M:%-S")
            data1 = data1+timedelta(seconds = 1)
            data2o = data1+timedelta(seconds = 1)
            print(data1, data2o)
            requested_data = Data.objects.filter(name = reqname, timestamp__gte = data1, timestamp__lte=data2o).exclude(frame__exact='')[:1]
            print(requested_data)
            serializer = DataSerializer(requested_data, many=True)
            #print(serializer.data)
            lista.append(serializer.data)
        jsonlist = json.dumps(lista)
        return Response(data=jsonlist, status=status.HTTP_200_OK)

#home of the web interface
def index(request):
    num_frames = Data.objects.count()
    num_cameras = Data.objects.values('name').annotate(count=Count('name')).count()

    context = {
        'num_frames' : num_frames,
        'num_cameras' : num_cameras,
    }

    return render(request, 'index.html', context = context)

#web - show list of registered cameras
class CameraList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'cameras_list.html'

    def get(self, request):
        queryset = Data.objects.values('name').distinct()
        #print(queryset)
        return Response({'cameras': queryset})

#web - show all frames for a given camera
def camera_frames(request, name):
    requested_data = Data.objects.all().filter(name = name).order_by('timestamp')
    #print(requested_data)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(requested_data, 50) # 50 per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'camera_frames.html', context={ 'page_obj' : page_obj ,'frames': requested_data, 'name': name})

#web - show all frames for a given camera in a given interval
def camera_frames_interval(request, name, interval):
    print("input"+name, interval)
    interv = interval.split("$")
    sdate = interv[0].replace("_"," ")
    edate = interv[1].replace("_"," ")
    requested_data = Data.objects.all().filter(name = name, timestamp__gte = sdate, timestamp__lte=edate).order_by('timestamp')
    page_num = request.GET.get('page', 1)
    paginator = Paginator(requested_data, 50) # 50 per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'interval_frames.html', context={'page_obj' : page_obj , 'frames': requested_data, 'name': name, 'data1': sdate, 'data2': edate})

#web - create a video with the shown frames given the camera and interval
def create_video(request, name, interval):
    #refactors time interval
    interv = interval.split("$")
    sdate = interv[0].replace("_"," ")
    edate = interv[1].replace("_"," ")
    requested_data = Data.objects.all().filter(name = name, timestamp__gte = sdate, 
        timestamp__lte=edate).order_by('timestamp').values_list('path', 'frame', 'name')
    #formats time interval for db entry
    interval_db = sdate+'-'+edate
    f = open('paths.txt', 'w+')
    for i in requested_data.iterator():
        f.write("file '../cameraApi/media/"+i[0]+i[1]+"' \n")
        f.write("duration 0.20 \n") #number can be parametric
    f.close
    #writes video with 
    video_name = '{name}-{interval}.mp4'.format(name= name, interval = interval)
    os.makedirs('../cameraApi/media/videos/{name}/'.format(name= name),exist_ok=True)
    try:
        ffmpeg.input('paths.txt',f='concat',safe=0).output('../cameraApi/media/videos/{name}/{video_name}'.format(name= name, video_name = video_name),c='libx264').run()
    except ffmpeg.Error as e:
        print(e.stdout)
        return render(request, 'video_error.html', context={'error' : e , 'name' : name})
    
    #creates db entry for the created video
    video_instance = Video.objects.create(name =name , path='/videos/{name}/'.format(name = name), video= video_name, time_interval= interval_db)
    return render(request, 'video_created.html', context={'name' : name})

#web - video gallery
def get_all_videos(request):
    requested_data = Video.objects.all()
    camera_list = Video.objects.values('name').distinct()
    page_num = request.GET.get('page', 1)
    paginator = Paginator(requested_data, 5) # 5 per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'video_gallery.html', context={'page_obj' : page_obj ,'videos' : requested_data, 'cameras' : camera_list})

#web - video gallery for a given camera
def get_camera_videos(request, name):
    requested_data = Video.objects.all().filter(name = name)
    page_num = request.GET.get('page', 1)
    paginator = Paginator(requested_data, 5) # 5 per page

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        # if page is not an integer, deliver the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if the page is out of range, deliver the last page
        page_obj = paginator.page(paginator.num_pages)
    return render(request, 'video_gallery.html', context={'page_obj' : page_obj , 'videos' : requested_data})