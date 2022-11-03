from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import UserForm
from .infra.users import get_users


@csrf_exempt
def index(request: HttpRequest) -> HttpResponse:

    user_form: UserForm
    values: dict = {}

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
        values = {
            'form': user_form,
            'users': get_users(),  # userを取得(sqlAlchemyを使用)
        }
    except Exception as e:  # エラー処理
        print(e)

    return render(request, 'index.html', values)
