import json

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from project import api
from project.models import Monitor, MonitorType

def index(request):

    # MonitorType.create('video')
    # MonitorType.create('picture')
    # MonitorType.create('slider', {'interval': 'int'})

    # body = {
    #     'name': 'Монитор - 1',
    #     'monitor_type': 'video',
    #     'values': ['test_video.mp4']
    # }
    # Monitor.create(**body)
    # body = {
    #     'name': 'Монитор - 2',
    #     'monitor_type': 'picture',
    #     'values': ['priroda-1.jpg']
    # }
    # Monitor.create(**body)
    # body = {
    #     'name': 'Реклама',
    #     'monitor_type': 'slider',
    #     'values': ['priroda-1.jpg', 'priroda-2.jpg', 'priroda-3.jpg'],
    #     'parameters': {'interval': 15}
    # }
    # Monitor.create(**body)

    return render(request, "starko/index.html")

def get(request):
    if request.method == "POST":
        monitors = Monitor.get(all=True)
        if monitors:
            return HttpResponse(json.dumps([monitor.serialize() for monitor in monitors]))
        else:
            return HttpResponse(json.dumps([]))
    else:
        return HttpResponseRedirect('/')

def create(request): #Попытка реализовать функцию создания, но потом понял, что слишком долго буду замарачиваться с загрузкой видео, так что просто оставил тут
    if request.method == "POST":
        body = api.get_body(request)
        answer = {
            'success': False,
            'error': '',
            'data': {}
        }
        monitor = Monitor.create(**body)
        if monitor:
            answer['success'] = True
            answer['data'] = monitor.serialize()
        else:
            answer['error'] = "Произошла непредвиденная ошибка"
        
        return HttpResponse(json.dumps(answer))
    else:
        return HttpResponseRedirect('/')