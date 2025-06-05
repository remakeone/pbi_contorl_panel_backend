from app import db
from datetime import datetime


class Report(db.Model):
    """
    报表模型类
    存储Power BI报表的元数据信息
    """
    __tablename__ = 'reports'
    
    # 基本信息字段
    id = db.Column(db.Integer, primary_key=True)  # 报表ID
    name = db.Column(db.String(100), nullable=False)  # 报表名称
    description = db.Column(db.Text)  # 报表描述
    powerbi_id = db.Column(db.String(256), nullable=False)  # Power BI报表ID

    # 状态字段
    is_active = db.Column(db.Boolean, default=True)  # 是否激活
    is_hide_report = db.Column(db.Boolean, default=True)  # 是否为隐藏报表

    # 时间字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间

    # 关系定义
    tags = db.relationship('Tag', secondary='report_tags', backref='reports')

    def to_dict(self, need_pbi_id=False):
        """
        将报表对象转换为字典格式
        Returns:
            dict: 包含报表信息的字典
        """

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'powerbi_id': self.powerbi_id if need_pbi_id else None,
            'is_active': self.is_active,
            'is_hide_report': self.is_hide_report,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'tags': [tag.name for tag in self.tags]
        }