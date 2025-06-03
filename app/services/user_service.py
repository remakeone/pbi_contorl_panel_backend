from app.models import User, RoleGroup, UserRoleGroup
from app import db

class UserService:
    """
    用户服务类
    处理用户相关的业务逻辑
    """
    
    @staticmethod
    def get_all_users():
        """
        获取所有用户
        
        Returns:
            list: 用户对象列表
        """
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """
        根据ID获取用户
        
        Args:
            user_id: 用户ID
            
        Returns:
            User: 用户对象
            
        Raises:
            404: 如果用户不存在
        """
        return User.query.get_or_404(user_id)
    
    @staticmethod
    def create_user(data):
        """
        创建新用户
        
        Args:
            data: 用户数据字典
            
        Returns:
            User: 创建的用户对象
            
        Raises:
            ValueError: 如果用户名已存在
        """
        raise ValueError("该接口已弃用")
        if User.query.filter_by(username=data['username']).first():
            raise ValueError("用户名已存在")
            
        user = User(
            username=data['username'],
            email=data.get('email'),
            password=data['password']  # 注意：实际应用中应该对密码进行加密
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id, data):
        """
        更新用户信息
        
        Args:
            user_id: 用户ID
            data: 用户数据字典
            
        Returns:
            User: 更新后的用户对象
            
        Raises:
            404: 如果用户不存在
            ValueError: 如果用户名已存在
        """
        user = User.query.get_or_404(user_id)
        
        if 'name' in data and data['name'] != user.name:
            if User.query.filter_by(name=data['name']).first():
                raise ValueError("用户名已存在")
            user.name = data['name']

        filter_fields = ['name', 'email', 'role','is_active']
        for field in filter_fields:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()
        UserService.add_user_to_role_groups(user_id, data.get('role_group_ids', []))

        return user
    
    @staticmethod
    def delete_user(user_id):
        """
        删除用户
        
        Args:
            user_id: 用户ID
            
        Raises:
            404: 如果用户不存在
        """
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
    
    @staticmethod
    def get_user_role_groups(user_id):
        """
        获取用户所属的所有角色组
        
        Args:
            user_id: 用户ID
            
        Returns:
            list: 角色组对象列表
            
        Raises:
            404: 如果用户不存在
        """
        user = User.query.get_or_404(user_id)
        return user.role_group
    
    @staticmethod
    def add_user_to_role_groups(user_id, role_group_ids):
        """
        将用户添加到多个角色组
        
        Args:
            user_id: 用户ID
            role_group_ids: 角色组ID列表
            
        Raises:
            404: 如果用户或角色组不存在
        """
        user = User.query.get_or_404(user_id)
        role_groups = RoleGroup.query.filter(RoleGroup.id.in_(role_group_ids)).all()
        
        for role_group in role_groups:
            if role_group not in user.role_groups:
                user.role_groups.append(role_group)

        for role_group in user.role_groups:
            if role_group not in role_groups:
                user.role_groups.remove(role_group)
                
        db.session.commit()
    
    @staticmethod
    def remove_user_from_role_group(user_id, role_group_id):
        """
        将用户从角色组中移除
        
        Args:
            user_id: 用户ID
            role_group_id: 角色组ID
            
        Raises:
            404: 如果用户或角色组不存在
        """
        user = User.query.get_or_404(user_id)
        role_group = RoleGroup.query.get_or_404(role_group_id)
        
        if role_group in user.role_group:
            user.role_groups.remove(role_group)
            db.session.commit() 