from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserData
from .forms import UserForm
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import UserDetailSerializer, UserSimpleSerializer

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
                user = authenticate(user, username=username, password=password)
                login(request, user)
                return redirect('index')
        return render(request, 'registration.html', {'invalid': True, 'form': user_form})

    def get(self, request):
        return render(request, 'registration.html', {'invalid': False, 'form': UserForm()})


@login_required(login_url="login")
def index(request):
    return render(request, "index.html")


def user_logout(request):
    logout(request)
    return redirect('index')


