from django.http import HttpResponse
from django.shortcuts import render
from .forms import UserForm
from .infra.users import get_users


def index(request):
    return HttpResponse('Hello Sample')


def login(request):

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_form.save(commit=True)
        print('hogehoge')
    else:
        user_form = UserForm()

    return render(request, 'login.html', {'form': user_form})


def users(request):
    values = {'users': get_users()}
    return render(request, 'users.html', values)
