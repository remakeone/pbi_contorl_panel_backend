# Power BI控制面板后端开发指南

## 项目介绍

### 项目背景
本项目是一个基于Power BI的报表控制面板系统，主要目标是通过自建的用户管理和权限控制系统，结合Power BI的公共链接模式，实现企业级报表的安全访问和展示。

### 核心功能
1. **报表管理**
   - 报表列表展示
   - 报表详情查看
   - 报表权限控制
   - 报表访问记录

2. **安全机制**
   - 自定义用户认证
   - 基于角色的权限控制
   - 报表访问控制
   - 防止未授权分享

3. **用户体验**
   - 统一的报表访问入口
   - 简洁的用户界面
   - 响应式设计
   - 实时数据更新

### 技术架构
- **前端**：Vue 3 + Element Plus
- **后端**：Python Flask
- **数据库**：PostgreSQL
- **报表集成**：Power BI Embedded

### 开发阶段
目前项目处于第一阶段，主要实现：
1. 基础的报表管理功能
2. 报表展示功能
3. 简单的访问控制

后续阶段将实现：
1. 完整的用户认证系统
2. 细粒度的权限控制
3. 报表使用统计
4. 更多自定义功能

## 环境准备

### 1. 安装必要的软件
- Python 3.8+
- PostgreSQL 12+
- Git

### 2. 创建项目目录
```bash
mkdir pbi_control_backend
cd pbi_control_backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 创建项目结构
```bash
pbi_control_backend/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── report.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── reports.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── report_service.py
│   └── utils/
│       └── __init__.py
├── config.py
├── .env
├── requirements.txt
└── run.py
```

## 具体实现步骤

### 1. 创建requirements.txt
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-CORS==4.0.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
Flask-Login==0.6.3
PyJWT==2.8.0
requests==2.31.0
```

### 2. 创建.env文件
```
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://username:password@localhost:5432/pbi_control
SECRET_KEY=your-secret-key
DINGTALK_APP_KEY=your_app_key
DINGTALK_APP_SECRET=your_app_secret
DINGTALK_REDIRECT_URI=http://your-domain/auth/dingtalk/callback
```

### 3. 配置文件 (config.py)
```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_HEADERS = 'Content-Type'
    DINGTALK_APP_KEY = os.getenv('DINGTALK_APP_KEY')
    DINGTALK_APP_SECRET = os.getenv('DINGTALK_APP_SECRET')
    DINGTALK_REDIRECT_URI = os.getenv('DINGTALK_REDIRECT_URI')
```

### 4. 应用初始化 (app/__init__.py)
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    
    from app.routes import register_routes
    register_routes(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    return app
```

### 5. 数据模型 (app/models/report.py)
```python
from app import db
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    powerbi_id = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'powerbi_id': self.powerbi_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
```

### 6. 服务层 (app/services/report_service.py)
```python
from app.models.report import Report
from app import db

class ReportService:
    @staticmethod
    def get_all_reports():
        return Report.query.all()
    
    @staticmethod
    def get_report_by_id(report_id):
        return Report.query.get_or_404(report_id)
    
    @staticmethod
    def create_report(data):
        report = Report(**data)
        db.session.add(report)
        db.session.commit()
        return report
    
    @staticmethod
    def update_report(report_id, data):
        report = Report.query.get_or_404(report_id)
        for key, value in data.items():
            setattr(report, key, value)
        db.session.commit()
        return report
    
    @staticmethod
    def delete_report(report_id):
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit()
```

### 7. 路由实现 (app/routes/reports.py)
```python
from flask import Blueprint, jsonify, request
from app.services.report_service import ReportService

reports = Blueprint('reports', __name__)

@reports.route('/api/reports', methods=['GET'])
def get_reports():
    reports = ReportService.get_all_reports()
    return jsonify([report.to_dict() for report in reports])

@reports.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report(report_id):
    report = ReportService.get_report_by_id(report_id)
    return jsonify(report.to_dict())

@reports.route('/api/reports', methods=['POST'])
def create_report():
    data = request.get_json()
    report = ReportService.create_report(data)
    return jsonify(report.to_dict()), 201

@reports.route('/api/reports/<int:report_id>', methods=['PUT'])
def update_report(report_id):
    data = request.get_json()
    report = ReportService.update_report(report_id, data)
    return jsonify(report.to_dict())

@reports.route('/api/reports/<int:report_id>', methods=['DELETE'])
def delete_report(report_id):
    ReportService.delete_report(report_id)
    return '', 204
```

### 8. 路由注册 (app/routes/__init__.py)
```python
from app.routes.reports import reports

def register_routes(app):
    app.register_blueprint(reports)
```

### 9. 应用入口 (run.py)
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

### 10. 测试数据脚本 (test_data.py)
```python
from app import create_app, db
from app.models.report import Report

app = create_app()

def create_test_data():
    with app.app_context():
        # 清除现有数据
        db.session.query(Report).delete()
        
        # 创建测试报表
        reports = [
            Report(
                name='销售报表',
                description='月度销售数据分析',
                powerbi_id='sales-report-id'
            ),
            Report(
                name='库存报表',
                description='实时库存状态',
                powerbi_id='inventory-report-id'
            )
        ]
        
        db.session.bulk_save_objects(reports)
        db.session.commit()

if __name__ == '__main__':
    create_test_data()
```

### 11. 钉钉登录集成

#### 11.1 更新依赖
```bash
# 添加到 requirements.txt
Flask-Login==0.6.3
PyJWT==2.8.0
requests==2.31.0
```

#### 11.2 钉钉配置
1. 在`.env`文件中添加钉钉配置：
```
DINGTALK_APP_KEY=your_app_key
DINGTALK_APP_SECRET=your_app_secret
DINGTALK_REDIRECT_URI=http://your-domain/auth/dingtalk/callback
```

2. 在`config.py`中添加配置：
```python
class Config:
    # ... 现有配置 ...
    DINGTALK_APP_KEY = os.getenv('DINGTALK_APP_KEY')
    DINGTALK_APP_SECRET = os.getenv('DINGTALK_APP_SECRET')
    DINGTALK_REDIRECT_URI = os.getenv('DINGTALK_REDIRECT_URI')
```

#### 11.3 用户模型 (app/models/user.py)
```python
from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    dingtalk_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # admin, user, editor
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def has_permission(self, permission):
        if self.role == 'admin':
            return True
        
        permission_map = {
            'user': ['view_reports'],
            'editor': ['view_reports', 'edit_reports'],
            'admin': ['view_reports', 'edit_reports', 'manage_users']
        }
        
        return permission in permission_map.get(self.role, [])
```

#### 11.4 钉钉认证服务 (app/services/auth_service.py)
```python
import requests
from app import db
from app.models.user import User
from datetime import datetime
from config import Config

class DingtalkAuthService:
    @staticmethod
    def get_access_token():
        """获取钉钉访问令牌"""
        url = "https://oapi.dingtalk.com/gettoken"
        params = {
            "appkey": Config.DINGTALK_APP_KEY,
            "appsecret": Config.DINGTALK_APP_SECRET
        }
        response = requests.get(url, params=params)
        return response.json().get("access_token")

    @staticmethod
    def get_user_info(code):
        """获取用户信息"""
        # 1. 获取用户token
        token_url = "https://oapi.dingtalk.com/sns/gettoken"
        params = {
            "appkey": Config.DINGTALK_APP_KEY,
            "appsecret": Config.DINGTALK_APP_SECRET
        }
        response = requests.get(token_url, params=params)
        access_token = response.json().get("access_token")

        # 2. 获取用户信息
        user_info_url = "https://oapi.dingtalk.com/sns/getuserinfo"
        params = {
            "access_token": access_token,
            "code": code
        }
        response = requests.get(user_info_url, params=params)
        return response.json()

    @staticmethod
    def login_or_create_user(dingtalk_info):
        """登录或创建用户"""
        user = User.query.filter_by(dingtalk_id=dingtalk_info['unionid']).first()
        
        if not user:
            user = User(
                dingtalk_id=dingtalk_info['unionid'],
                name=dingtalk_info.get('nick', '未命名'),
                email=dingtalk_info.get('email', '')
            )
            db.session.add(user)
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user
```

#### 11.5 认证路由 (app/routes/auth.py)
```python
from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required
from app.services.auth_service import DingtalkAuthService
from urllib.parse import urlencode

auth = Blueprint('auth', __name__)

@auth.route('/api/auth/dingtalk/url', methods=['GET'])
def get_dingtalk_url():
    """获取钉钉登录二维码URL"""
    url = f"https://oapi.dingtalk.com/connect/qrconnect"
    params = {
        "appid": Config.DINGTALK_APP_KEY,
        "response_type": "code",
        "scope": "snsapi_login",
        "redirect_uri": Config.DINGTALK_REDIRECT_URI,
    }
    return jsonify({"url": url + "?" + urlencode(params)})

@auth.route('/api/auth/dingtalk/callback', methods=['POST'])
def dingtalk_callback():
    """处理钉钉回调"""
    code = request.json.get('code')
    if not code:
        return jsonify({'error': '无效的请求'}), 400

    try:
        user_info = DingtalkAuthService.get_user_info(code)
        if 'error' in user_info:
            return jsonify({'error': user_info['errmsg']}), 400

        user = DingtalkAuthService.login_or_create_user(user_info)
        login_user(user)

        return jsonify({
            'message': '登录成功',
            'user': {
                'id': user.id,
                'name': user.name,
                'role': user.role
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """用户登出"""
    logout_user()
    return jsonify({'message': '登出成功'})
```

#### 11.6 权限装饰器 (app/utils/decorators.py)
```python
from functools import wraps
from flask import jsonify
from flask_login import current_user

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'error': '请先登录'}), 401
            if not current_user.has_permission(permission):
                return jsonify({'error': '权限不足'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

## 部署步骤

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 初始化数据库
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 3. 创建测试数据
```bash
python test_data.py
```

### 4. 启动应用
```bash
flask run
```

## API测试

### 1. 获取所有报表
```bash
curl http://localhost:5000/api/reports
```

### 2. 获取特定报表
```bash
curl http://localhost:5000/api/reports/1
```

### 3. 创建新报表
```bash
curl -X POST http://localhost:5000/api/reports \
  -H "Content-Type: application/json" \
  -d '{"name":"新报表","description":"测试报表","powerbi_id":"test-id"}'
```

### 4. 更新报表
```bash
curl -X PUT http://localhost:5000/api/reports/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"更新后的报表"}'
```

### 5. 删除报表
```bash
curl -X DELETE http://localhost:5000/api/reports/1
```

## 注意事项

1. 确保PostgreSQL数据库已安装并正确配置
2. 检查.env文件中的数据库连接信息是否正确
3. 所有API响应使用JSON格式
4. 已配置CORS，支持前端跨域访问
5. 建议在开发环境中启用DEBUG模式
6. 定期备份数据库
7. 生产环境部署时更新SECRET_KEY
8. 添加适当的日志记录 