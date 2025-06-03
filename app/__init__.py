from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from config import get_config

# 初始化数据库
db = SQLAlchemy()

# 初始化登录管理器
login_manager = LoginManager()

def create_app():
    """
    创建并配置Flask应用
    Returns:
        app: Flask应用实例
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(get_config())
    
    # 初始化CORS
    CORS(app,
         supports_credentials=True,  # 允许携带凭证
         origins=[
             "http://localhost:5173",
         ],  # 明确指定允许的源
         methods=["GET", "POST", "PUT", "DELETE"],  # 允许的方法
         allow_headers=["Content-Type", "Authorization"]  # 允许的请求头
        )
    
    # 初始化SQLAlchemy
    db.init_app(app)

    with app.app_context():
        from app.models import RoleGroup, User, Report
        db.create_all()
        print('数据库表创建完成')

    # 初始化登录管理器
    login_manager.init_app(app)
    
    # 注册蓝图
    from app.routes import register_routes
    register_routes(app)
    
    # 用户加载回调
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    return app 