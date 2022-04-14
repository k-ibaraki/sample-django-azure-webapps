from typing import List

from sample.models import User
from aldjemy.orm import BaseSQLAModel
from aldjemy.core import get_engine
from sqlalchemy.orm import Session, sessionmaker


# SQLAlchemyを使ってデータを取得


def get_users() -> List[dict]:
    # Userが、DjangoのModel
    # User_sa=User.saが、SQLAlchemyのModel
    User_sa: BaseSQLAModel = User.sa

    # AldjemyでDjangoの設定からEngineを取ってきて、SQLAlchemyのsessionを取得
    session: Session = sessionmaker(bind=get_engine())()

    # SQLAlchemyでUserの全てgetする : session.query(User_sa).all()
    # -> 配列の各要素からdict形式でデータを取り出す : u.__dict__.items()
    # -> dictからSQLAlchemyが付与する一時情報を削除 : k != "_sa_instance_state"
    # いわゆる内包表記で書いています。Python特有の書き方なのでなれないと分かりにくいかもです。
    users: List[dict] = [{k: v for k, v in u.__dict__.items() if k != "_sa_instance_state"}
                         for u in session.query(User_sa).all()]

    # session.query(User_sa).all()は下記でも動きます。（この場合sessionの定義は不要にできます）
    # User_sa.query().all()
    return users
