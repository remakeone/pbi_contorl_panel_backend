from app.routes.reports import reports
from app.routes.auth import auth
from app.routes.role_groups import role_groups
from app.routes.users import users

def register_routes(app):
    """
    注册所有蓝图路由
    Args:
        app: Flask应用实例
    """
    # 注册报表相关路由
    app.register_blueprint(reports)
    # 注册认证相关路由
    app.register_blueprint(auth)
    # 注册角色组相关路由
    app.register_blueprint(role_groups)
    # 注册用户相关路由
    app.register_blueprint(users)