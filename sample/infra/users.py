from sample.models import User
from aldjemy.orm import BaseSQLAModel

# SQLAlchemyを使ってデータを取得


def get_users() -> list:
    # Userが、DjangoのModel
    # User_sa=User.saが、SQLAlchemyのModel
    User_sa: BaseSQLAModel = User.sa

    # SQLAlchemyでUserの全てgetする : User_sa.query().all()
    # -> 配列の各要素からdict形式でデータを取り出す : u.__dict__.items()
    # -> dictからSQLAlchemyが付与する一時情報を削除 : k != "_sa_instance_state"
    # いわゆる内包表記で書いています。Python特有の書き方なのでなれないと分かりにくいかもです。
    users = [{k: v for k, v in u.__dict__.items() if k != "_sa_instance_state"}
             for u in User_sa.query().all()]
    return users
