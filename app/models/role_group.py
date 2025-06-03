from app import db
from app.models.user_role_group import UserRoleGroup


class RoleGroup(db.Model):
    """
    角色组模型
    用于管理用户组和报表的可见性关系
    """
    __tablename__ = 'role_groups'

    id = db.Column(db.Integer, primary_key=True, comment='主键ID')
    name = db.Column(db.String(100), nullable=False, comment='角色组名称')
    description = db.Column(db.String(500), nullable=True, comment='角色组描述')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), comment='更新时间')

    # 与用户的关联关系
    users = db.relationship('User', secondary='user_role_groups', backref=db.backref('role_groups', lazy='dynamic'))

    # 与报表的关联关系
    visible_reports = db.relationship('Report', secondary='group_visible_reports', backref=db.backref('visible_groups', lazy='dynamic'))

    def __init__(self, name, description=None):
        """
        初始化角色组对象
        
        Args:
            name: 角色组名称
            description: 角色组描述
        """
        self.name = name
        self.description = description

    def to_dict(self,simple=False):
        """
        将角色组对象转换为字典
        
        Returns:
            dict: 包含角色组信息的字典
        """
        if simple:
            return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None
            }
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'users': [user.to_dict() for user in self.users],  # 包含组内所有用户信息
            'user_count': len(self.users),  # 用户数量
            'reports': [report.id for report in self.visible_reports],  # 可见报表ID列表
            'visible_reports': [report.id for report in self.visible_reports]  # 可见报表ID列表
        }

    def __repr__(self):
        """
        返回角色组对象的字符串表示
        
        Returns:
            str: 角色组对象的字符串表示
        """
        return f'<RoleGroup {self.name}>'


# 关联表
group_visible_reports = db.Table('group_visible_reports',
                                 db.Column('group_id', db.Integer, db.ForeignKey('role_groups.id'), primary_key=True),
                                 db.Column('report_id', db.Integer, db.ForeignKey('reports.id'), primary_key=True)
                                 )