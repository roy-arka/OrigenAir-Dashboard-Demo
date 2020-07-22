from django.views.generic import CreateView 
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView 
from django.views.generic.detail import DetailView 
from django.views.generic.edit import DeleteView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.urls import reverse
from . models import Sensor, Record
from . import forms
from django.shortcuts import get_object_or_404
from organization.models import Organization
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import datetime

#Create your views here.

class SensorAdminRequiredMixin(UserPassesTestMixin, LoginRequiredMixin):
    def test_func(self):
        full_path = self.request.get_full_path()
        split_full_path = full_path.split("/")
        org_slug = split_full_path[3]
        org = Organization.objects.get(slug=org_slug)
        return self.request.user == org.admin
    
class CreateSensor(SensorAdminRequiredMixin, CreateView):
    model = Sensor
    form_class = forms.SensorCreateForm
    template_name = 'sensor/sensor_create.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organization = self.request.user.person.organization
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('sensor:single', kwargs={'slug': self.object.organization.slug, 'pk': self.object.pk})
        
class SensorDetail(LoginRequiredMixin, DetailView):
    model = Sensor
    template_name = 'sensor/sensor_detail.html'

class UpdateSensor(SensorAdminRequiredMixin, UpdateView):
    model = Sensor
    form_class = forms.SensorUpdateForm
    template_name = 'sensor/sensor_update.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.organization = self.request.user.person.organization
        self.object.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('sensor:single', kwargs={'slug': self.object.organization.slug, 'pk': self.object.pk})

class SensorList(LoginRequiredMixin, ListView):
    model = Sensor
    template_name = 'sensor/sensor_list.html'

class DeleteSensor(SensorAdminRequiredMixin, DeleteView):
    model = Sensor
    template_name = 'sensor/sensor_delete.html'
     
    def get_success_url(self):
        return reverse_lazy('sensor:all', kwargs={'slug': self.object.organization.slug})


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class SensorDetailAPI(APIView):
    # authentication_classes = (authentication.SessionAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        return (get_object_or_404(Sensor, pk=pk))


    def get(self, request, *args, **kwargs):
        sensor = self.get_object(self.kwargs.get('pk'))

        data = {
            "name": sensor.name,
            "organization": sensor.organization.name,
            "type": sensor.sensor_type,
            "value": sensor.value,
            "min": sensor.threshold_min,
            "max": sensor.threshold_max,
        
        }
        return Response(data)

    
    def put(self, request, *args, **kwargs):
        sensor = self.get_object(self.kwargs.get('pk'))


        value = request.data['value']
        sensor.value = value
        sensor.save()

        data = {
            "name": sensor.name,
            "value": sensor.value,
            "updated": "True"
        }

        return Response(data)

class RecordLastDayAPI(APIView):

    def get_object(self, pk):
        return (get_object_or_404(Sensor, pk=pk))

    def get(self, request, *args, **kwargs):
        sensor = self.get_object(self.kwargs.get('pk'))
        time_24_hours_ago = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        records = Record.objects.filter(sensor__id=sensor.id, created_at__gte=time_24_hours_ago)

        data = { 
            "sensor": sensor.name,
        }

        for record in records:
            data[record.pk] = {
                "created_at": record.created_at,
                "value": record.value,
            }
            
        return Response(data)

