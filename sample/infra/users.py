from sample.models import User


def get_users() -> list:
    users = [{k: v for k, v in u.__dict__.items() if k != "_sa_instance_state"}
             for u in User.sa.query().all()]
    return users
