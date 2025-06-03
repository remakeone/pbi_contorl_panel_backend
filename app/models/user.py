from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    """
    用户模型类
    继承自Flask-Login的UserMixin和SQLAlchemy的Model
    用于存储用户信息和处理用户认证
    """
    __tablename__ = 'users'
    
    # 用户基本信息字段
    id = db.Column(db.Integer, primary_key=True)  # 用户ID
    dingtalk_id = db.Column(db.String(100), unique=True, nullable=True)  # 钉钉用户唯一标识
    name = db.Column(db.String(100))  # 用户姓名
    email = db.Column(db.String(120))  # 用户邮箱
    
    # 用户权限相关字段
    role = db.Column(db.String(20), default='user')  # 用户角色：admin-管理员, editor-编辑者, user-普通用户
    is_active = db.Column(db.Boolean, default=True)  # 用户是否激活
    
    # 时间相关字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 用户创建时间
    last_login = db.Column(db.DateTime)  # 最后登录时间

    def has_permission(self, permission):
        """
        检查用户是否具有特定权限
        Args:
            permission (str): 需要检查的权限名称
        Returns:
            bool: 是否具有权限
        """
        # 管理员和编辑者拥有所有权限
        if self.role == 'admin' or self.role == 'editor':
            return True
        
        # 定义各角色的权限映射
        permission_map = {
            'user': ['view_reports'],  # 普通用户只能查看报表
        }
        
        return permission in permission_map.get(self.role, [])

    def to_dict(self):
        """
        将用户对象转换为字典格式
        Returns:
            dict: 包含用户信息的字典
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            "is_bind": not self.dingtalk_id == self.name,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'last_login': self.last_login if self.last_login else None,
            "role_groups": [group.to_dict(simple=True) for group in self.role_groups] if self.role_groups else []
        }

    def can_view_report(self, report):
        """
        检查用户是否可以查看指定报表
        
        Args:
            report: 需要检查的报表对象
        
        Returns:
            bool: 是否可以查看报表
        """
        # 管理员可以查看所有报表
        if self.role == 'admin':
            return True
            
        # 检查用户的角色组是否可以查看该报表
        for role_group in self.role_groups:
            if report in role_group.visible_reports:
                return True
                
        return False

