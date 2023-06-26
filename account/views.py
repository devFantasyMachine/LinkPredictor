from django.contrib.auth import authenticate, logout as _logout, login as signin
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from .serializers import UserRegistrationSerializer


def logout(request):

    _logout(request)

    return redirect("/")


@csrf_exempt
def login(request):
    email = ''
    password = ''
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
        if 'password' in request.POST:
            password = request.POST['password']

        user = authenticate(request, email=email, password=password)
        print(user)

        if user is not None:
            signin(request, user)

            return redirect("/home")

        else:

            return render(request, 'welcome/login.html', {"email": email, "error": True})

    return render(request, 'welcome/login.html', {})


@csrf_exempt
def register(request):
    email = ''
    password = ''
    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
        if 'password' in request.POST:
            password = request.POST['password']

        print(request.POST)
        serializer = UserRegistrationSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = authenticate(request, email=email, password=password)
        print(user)

        if user is not None:
            signin(request, user)

            return redirect("/home")

        else:

            return render(request, 'welcome/register.html', {"email": email, "error": True})

    return render(request, 'welcome/register.html', {})


@csrf_exempt
def index(request):

    user = request.user

    if not user.is_authenticated:
        user = None

    return render(request, 'welcome/index.html', {"user": user})


