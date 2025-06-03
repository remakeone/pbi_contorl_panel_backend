from app import db
from datetime import datetime
import pytz


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
    
    # 时间字段
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    # visible_groups关系由RoleGroup的backref定义

    def to_dict(self, need_pbi_id=False):
        """
        将报表对象转换为字典格式
        Returns:
            dict: 包含报表信息的字典
        """
        def format_time(dt):
            # 如果时间对象存在，转换为 YYYY-MM-DD HH:MM:SS 格式字符串，否则返回 None
            return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'powerbi_id': self.powerbi_id if need_pbi_id else None,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }