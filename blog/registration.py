from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from blog.forms import LoginForm
from blog.models import CustomUser


def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = CustomUser.objects.create_user(username=username, password=password2)
            return HttpResponse('Пользователь успешно создан')
        else:
            return HttpResponse('Пароли не совпадают')
    return render(request, 'registration.html', locals())


def log_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm
    return render(request, 'log_in.html', {'form': form})
