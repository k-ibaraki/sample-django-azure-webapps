# sample-django-azure-webapps

## Architecture

![](docs/Architecture.drawio.png)

## アプリ概要
- Python + Djangoのwebアプリ
- SQL Databaseと接続
- Container

# アプリ起動までの最低限の設定

## Poetryを使って必要なライブラリのインストール
Pythonのパッケージ管理にpoetryを使っています。
- https://cocoatomo.github.io/poetry-ja/

### Poetryのインストール
```sh
pip install poetry
```

### Poetryを使って必要なライブラリのインストール
`pyproject.toml`に書かれた内容に従って、必要なライブラリがインストールされます。
```sh
poetry update
```

## 　DBの準備
- テスト用のSQL Serverを用意し、`データベース`と`ユーザー`作成してください。

## SQL Server接続用にODBC Driverのインストール
下記URLを参照し、アプリを実行する環境に`Microsoft ODBC Driver 18 for SQL Server`をインストールしてください。
- https://docs.microsoft.com/ja-jp/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15


## Djangoの設定
- Djangoに下記のプロジェクトとアプリを追加してサンプルを作りました。
  - プロジェクト : `sampleProject`
  - アプリ : `sample`
- Djangoの設定は`sampleProject/setting.py`で設定できます。
- 今回最低限必要な設定は、環境変数に外に出しています。
- ローカルテスト用の環境変数は、`.env`fileで設定できます。

### `.env`の設定
- `.env.sample`ファイルを`.env`というfileにコピーしてください。
- `.env`に下記の必要な設定を入力してください。
```:.env
# Djangoアプリのシークレットキーになります
SECRET_KEY=

# Djangoアプリが起動できるHOST名
ALLOWED_HOSTS=localhost,127.0.0.1

# SQL ServerのHOST
MS_DB_HOST=localhost

# SQL ServerのPort
MS_DB_PORT=1433

# SQL ServerのDB名
MS_DB_NAME=django-sample-sql-db

# SQL Serverのユーザー名
MS_DB_USER=user

# SQL Serverのパスワード
MS_DB_PASSWORD=Password

# SQL Serverのドライバ名
MS_DB_DRIVER="ODBC Driver 18 for SQL Server"

# ローカルのSQL Serverで、SSLエラーが出るときは追加してください。
# 基本的に本番環境には設定しないでください。
MS_DB_EXTRA_PARAMS="TrustServerCertificate=yes"
```

## DB Migration
下記コマンドで、DBのMigrationを実施してください
```sh
poetry run python manage.py migrate
```

## アプリ起動
下記コマンドでアプリを起動してください。
- 開発用
```sh
poetry run python manage.py runserver
```

- （補足）本番用では`manage.py runserver`での起動は推奨されていませんので、`gunicorn`からも起動できるようにしています。
```sh
poetry run gunicorn sampleProject.asgi:application -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## サンプルアプリのDocker imageの作成・ローカルでの起動
- ルートディレクトリにある`DockerFile`にdockerイメージを作成する設定が入っていますので、`docker build` コマンドでdockerイメージを作成することができます。
- 今回は、更にローカルで楽に起動できるように`compose.yml`も作りましたので、ルートディレクトリで下記コマンドで起動アプリを起動できます。
  - (注意)環境変数は`.env`ファイルから取得するようにしていますので、先に`.env`の設定をお願いします。
- ビルド
```sh
docker compose build
```
- 起動
```sh
docker compose up
```

# SQL Serverもdockerで動かす方法について

## SQL Serveの起動
- `sql_db_docker`配下に、SQL Server用の`compose.yml`を作成しています。
- `sql_db_docker`配下に移動して、起動してください
```sh
cd sql_db_docker
docker compose up
```

## Databaseとユーザーの作成
- 上記の`compose.yml`は`SQL Server`の立ち上げまでしかしてないので、Databaseとユーザーの作成は`localhost:1433`に接続してsqlコマンドを実行してください。

## アプリケーション側のcompose.ymlにネットワークの設定を追加
- dbとアプリの両方を`docker`で動かす場合、ネットワークの設定が必要です。
- アプリ用の`compose.yml`(ルート直下)でコメントアウトしてある箇所を有効化することで、ネットワークの設定が出来ます。
- このとき、アプリから指定するsql serverのホスト名は、docker上でのサービス名になります。具体的には`db`です。


# Djangoの設定について
このサンプルで実施したDjangoの設定について説明します。

## Djangoの初期設定
- djangoインストール
```
poetry add django
```
- プロジェクト作る
```
poetry run django-admin startproject sampleProject .
```
- sampleアプリ追加
```
poetry run python manage.py startapp sample
```
```py:sampleProject/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sample', # add
]
```
- sampleアプリを適当に書く
```py:sample/views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse('Hello Sample')
```

- ルーティング
```py:sampleProject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sample/', include('sample.urls')) # add
]
```
```py:sample/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
]
```

## Djangoの起動
- migrate
```
poetry run python manage.py migrate
```
- 起動
```
poetry run python manage.py runserver
```
-> `http://localhost:8000/sample` にアクセスすると起動

## Gunicornを導入
`python manage.py runserver` は開発用の為、アプリケーションサーバーにGunicornを導入する
```
poetry add uvicorn gunicorn
```
- 起動
```
gunicorn sampleProject.asgi:application -w 2 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## SQL Server接続の設定
DjangoのORMとSQLAlchemyの両方を使えるようにしています。

### mssql-djangoをインストール
DjangoにMSSQLを追加できるようにするライブラリです。
- https://docs.microsoft.com/en-us/samples/azure-samples/mssql-django-samples/mssql-django-samples/
```
poetry add mssql-django
```

### aldjemy
DjangoとSQLAlchemyを接続するライブラリです。
- https://github.com/aldjemy/aldjemy
```
poetry add aldjemy
```

### Setting.pyを設定

```py:sampleProject/settings.py
ALDJEMY_ENGINES = {
    "mssql": 'mssql+pyodbc'
}
DATABASES = {
    "default": {
        "ENGINE": "mssql",
        "NAME": os.getenv('MS_DB_NAME', ''),
        "USER": os.getenv('MS_DB_USER', ''),
        "PASSWORD": os.getenv('MS_DB_PASSWORD', ''),
        "HOST": os.getenv('MS_DB_HOST', 'localhost'),
        "PORT": os.getenv('MS_DB_PORT', '1433'),
        "OPTIONS": {
            "driver": os.getenv('MS_DB_DRIVER', 'ODBC Driver 18 for SQL Server'),
            "extra_params": os.getenv('MS_DB_EXTRA_PARAMS', ''),
        },
    },
}
```
- 設定情報は環境変数へ外出ししています
  - ローカルでの動作は`.env.sample`ファイルを`.env`というfileにコピーして、`.env`に下記の必要な設定を入力してください。
  - AzureWebApps上では、`構成`の設定から環境変数を設定してください。
- `extra_params`はローカル実行時に、sslのセキュリティチェックを回避する為に追加しています。

### ODBCドライバーのインストール

- ローカルでアプリを実行する場合は、ODBCドライバーをインストールしてください
  - https://docs.microsoft.com/ja-jp/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15
- dockerはimage作成時にインストールするように`Dockerfile`に設定しています

### DB接続の使い方
`sample`配下のソースコードを参照してください。
- 今回のサンプルでは、PostはDjangoから直接、GetはSQLAlchemyを使っています。
  - 両方使えるというサンプルなので使い分けを推奨しているわけではありません。
- `models.py`に、Djangoの記法でModelを書いています。
```py:models.py
class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=16)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)
```
- `infra/users.py`に、SQLAlchemyを使ってUserを取得するコードを書いています。
  - 準備
    ```py:infra/users.py
    # Userが、DjangoのModel
    # User_sa=User.saが、SQLAlchemyのModel
    User_sa: BaseSQLAModel = User.sa
    # AldjemyでDjangoの設定からEngineを取ってきて、SQLAlchemyのsessionを取得
    session: Session = sessionmaker(bind=get_engine())()
    ```
  - Userの一覧をDBから取得できます
    ```py:infra/users.py
    session.query(User_sa).all()
    ```

- `views.py`の下記の部分で、Djangoを使ってUserを登録しています。
```py:view.py
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
```

## 構築に当たっての注意事項

### Djangoの`SECRET_KEY`
- `settings.py`に`SECRET_KEY`を設定しないと正しく動きません。
- 直書きは良くないので、環境変数に出しています。
- 配布にあたり、`.env.sample`に本物の`SECRET_KEY`を書いています。実運用での取り扱いにはご注意ください。
  - そのままは使わずに、再生成することをお勧めします。

### Djangoの`ALLOWED_HOSTS`
- `settings.py`の`ALLOWED_HOSTS`に、アプリが動作するホスト名を追加する必要があります。
- 環境変数で設定できるようにしています。

### `ALDJEMY_ENGINES`の追加
Aldjemyを使って、DjangoとSQLAlchemyを連携するには、`settings.py`に`ALDJEMY_ENGINES`の追加が必要です
```py:settings.py
ALDJEMY_ENGINES = {
    "mssql": 'mssql+pyodbc'
}
```

### DB設定にextra_paramsを追加
- DBとアプリを両方ローカルで動かした時、SSLの設定をしていないとデフォルトだとエラーになります。
- `settings.py`の`DATABASES`の設定で`extra_params`に`TrustServerCertificate=yes`を設定することで、SSLのチェックをスキップできます。
- 環境変数で`extra_params`を設定できるようにしています。

### `csrf`について
- Djangoでは標準で`CSRF`対策の機能が入っています。
- ですが、なぜか`Azure WebApps`にdeployすると、この機能により`POST`がエラーになってしまいました。
- `POST`を使用していいる関数に`@csrf_exempt`を追加して、機能を無効化しています。
- 具体的には`views.py`の下記箇所
```py:views.py
@csrf_exempt
def index(request: Request) -> HttpResponse:
```

# 使用している主なライブラリまとめ

## Poetry
Pythonのライブラリ管理ツール
- https://cocoatomo.github.io/poetry-ja/

## Django
PythonでメジャーなWebアプリケーションフレームワーク
- https://docs.djangoproject.com/ja/4.0/

## mssql-django
Django環境でSQL Databaseを使用する為のライブラリ
- https://docs.microsoft.com/en-us/samples/azure-samples/mssql-django-samples/mssql-django-samples/

## SQLAlchemy
PythonでメジャーなORM
- https://www.sqlalchemy.org

## Aldjemy
DjangoとSQLAlchemyを連携する為のライブラリ
- https://pypi.org/project/aldjemy/

## gunicorn
Python HTTP サーバー
- https://gunicorn.org

## python-dotenv
.envファイルから環境変数を読み出すライブラリ。開発用。
- https://pypi.org/project/python-dotenv/
