from app import db

class UserRoleGroup(db.Model):
    """
    用户与角色组的关联表模型
    用于维护用户和角色组之间的多对多关系
    """
    __tablename__ = 'user_role_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, comment='用户ID')
    role_group_id = db.Column(db.Integer, db.ForeignKey('role_groups.id', ondelete='CASCADE'), nullable=False, comment='角色组ID')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    
    # 添加唯一约束，确保一个用户在一个角色组中只能出现一次
    # __table_args__ = (
    #     db.UniqueConstraint('user_id', 'role_group_id', name='uix_user_role_group'),
    # )
    
    def __init__(self, user_id, role_group_id):
        """
        初始化用户角色组关联对象
        
        Args:
            user_id: 用户ID
            role_group_id: 角色组ID
        """
        self.user_id = user_id
        self.role_group_id = role_group_id
    
    def __repr__(self):
        """
        返回用户角色组关联对象的字符串表示
        
        Returns:
            str: 用户角色组关联对象的字符串表示
        """
        return f'<UserRoleGroup user_id={self.user_id} role_group_id={self.role_group_id}>' 