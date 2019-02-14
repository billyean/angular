from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import (Service)
from django.http import JsonResponse


# Create your views here.
@login_required
def service_base(request):
    return render(request, 'service/main.html', None)


@login_required
def service_list(request):
    print(request)
    if request.method == 'GET':
        services = list(Service.objects.all().order_by('create_time').values())
        data = dict()
        data['services'] = services
        return JsonResponse(data)
    else:
        print(request)
        service = Service.objects.create(name=request.POST['name'],
                                         time_type=request.POST['time_type'],
                                         rate=request.POST['rate'])
        service.save()
        return JsonResponse({
            'id': service.id,
            'name': service.name,
            'time_type': service.time_type,
            'rate': service.rate
        })


@login_required
def service_detail(request, service_id):
    service = Service.objects.get(id=service_id)
    if request.method == 'POST':
        if request.POST['name'] is not None:
            service.name = request.POST['name']
        if request.POST['time_type'] is not None:
            service.time_type = request.POST['time_type']
        if request.POST['rate'] is not None:
            service.rate = request.POST['rate']
        service.save()

        services = list(Service.objects.all().order_by('create_time').values())
        data = dict()
        data['services'] = services
        return JsonResponse(data)
    elif request.method == 'DELETE':
        service.delete()

    return JsonResponse({
        'id': service.id,
        'name': service.name,
        'time_type': service.time_type,
        'rate': service.rate
    })
