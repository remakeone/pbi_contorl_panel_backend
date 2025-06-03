from app import db

class GroupVisibleReport(db.Model):
    """
    角色组与报表的关联表模型
    用于维护角色组和报表之间的多对多关系，控制哪些报表对哪些角色组可见
    """
    __tablename__ = 'group_visible_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    role_group_id = db.Column(db.Integer, db.ForeignKey('role_groups.id', ondelete='CASCADE'), nullable=False, comment='角色组ID')
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id', ondelete='CASCADE'), nullable=False, comment='报表ID')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), comment='创建时间')
    
    # 添加唯一约束，确保一个角色组对一个报表只能设置一次可见性
    __table_args__ = (
        db.UniqueConstraint('role_group_id', 'report_id', name='uix_group_visible_report'),
    )
    
    def __init__(self, role_group_id, report_id):
        """
        初始化角色组可见报表关联对象
        
        Args:
            role_group_id: 角色组ID
            report_id: 报表ID
        """
        self.role_group_id = role_group_id
        self.report_id = report_id
    
    def __repr__(self):
        """
        返回角色组可见报表关联对象的字符串表示
        
        Returns:
            str: 角色组可见报表关联对象的字符串表示
        """
        return f'<GroupVisibleReport role_group_id={self.role_group_id} report_id={self.report_id}>' 