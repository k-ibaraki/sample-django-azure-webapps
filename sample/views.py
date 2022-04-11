from urllib.request import Request
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm
from .infra.users import get_users


@csrf_exempt
def index(request: Request) -> HttpResponse:

    user_form: UserForm
    valuse: dict = {}

    if request.method == 'POST':  # POSTされたときの処理
        try:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save(commit=True)  # DBにデータを保存
        except Exception as e:  # エラー処理
            print(e)
            user_form = UserForm()
    else:
        user_form = UserForm()

    try:
        valuse = {
            'form': user_form,
            'users': get_users(),  # userを取得(sqlAlchemyを使用)
        }
    except Exception as e:  # エラー処理
        print(e)

    return render(request, 'index.html', valuse)
