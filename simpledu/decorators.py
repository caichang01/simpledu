from flask import abort
from flask_login import current_user
from functools import wraps
from simpledu.models import User


def role_required(role):
    """
    带参数的装饰器，可以使用它来保护一个路由处理函数只能被具有特定角色的用户访问
    @role_required(User.ADMIN):
        def admin():
            pass
    :param role:
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 未登录或角色权限不符合触发404，不采用403的原因是不希望将路由暴露给不具有权限的用户
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorator


# 特定角色的装饰器
staff_required = role_required(User.ROLE_STAFF)
admin_required = role_required(User.ROLE_ADMIN)
