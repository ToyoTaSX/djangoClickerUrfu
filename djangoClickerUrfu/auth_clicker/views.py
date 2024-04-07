from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserForm
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserDetailSerializer, UserSimpleSerializer
from game_core_api import models as game_models

class UsersSimpleList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer

class UsersDetailsList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = "username"

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, "login.html", {"invalid": True})

    def get(self, request):
        return render(request, "login.html", {"invalid": False})


class UserRegistrationView(APIView):
    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password']
            existing_user = User.objects.filter(username=username)
            if len(existing_user) == 0:
                user = user_form.save()
                core = game_models.Core(user=user)
                core.save()
                user = authenticate(user, username=username, password=password)
                login(request, user)
                return redirect('index')
        return render(request, 'registration.html', {'invalid': True, 'form': user_form})

    def get(self, request):
        return render(request, 'registration.html', {'invalid': False, 'form': UserForm()})


def user_logout(request):
    logout(request)
    return redirect('index')


