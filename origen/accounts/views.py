from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms

# Create your views here.
class SignUp(CreateView):
    form_class = forms.PersonCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

class Login(CreateView):
    form_class = forms.PersonCreateForm
    template_name = 'accounts/login.html'


