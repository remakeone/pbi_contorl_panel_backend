from app.models.report import Report
from app import db
from flask_login import current_user

class ReportService:
    """
    报表服务类
    处理报表相关的业务逻辑
    """
    
    @staticmethod
    def get_all_reports():
        """
        获取当前用户有权限查看的所有报表

        Returns:
            list: 用户有权限查看的报表对象列表
        """
        all_reports = Report.query.filter_by(is_active=True).all()
        if current_user.is_authenticated and current_user.role == 'admin':
            return [report.to_dict() for report in all_reports]
        elif current_user.is_authenticated and current_user.role == 'editor':   # 对于编辑者，多返回一个报表id
            return [report.to_dict(need_pbi_id=True) for report in all_reports]
        return [report.to_dict() for report in all_reports if current_user.can_view_report(report)]

    @staticmethod
    def get_report_by_id(report_id):
        """
        根据ID获取报表
        
        Args:
            report_id: 报表ID
            
        Returns:
            Report: 报表对象
            
        Raises:
            404: 如果报表不存在
        """
        return Report.query.filter_by(id=report_id, is_active=True).first_or_404()
    
    @staticmethod
    def create_report(data):
        """
        创建新报表
        
        Args:
            data: 报表数据字典
            
        Returns:
            Report: 创建的报表对象
        """
        if 'powerbi_id' not in data:
            raise ValueError("powerbi_id为空")
        report = Report(**data)
        db.session.add(report)
        db.session.commit()
        return report
    
    @staticmethod
    def update_report(report_id, data):
        """
        更新报表信息
        
        Args:
            report_id: 报表ID
            data: 报表数据字典
            
        Returns:
            Report: 更新后的报表对象
            
        Raises:
            404: 如果报表不存在
        """
        report = Report.query.get_or_404(report_id)
        for key, value in data.items():
            if key == 'powerbi_id' and not value:
                continue
            if hasattr(report, key):
                setattr(report, key, value)
        db.session.commit()
        return report
    
    @staticmethod
    def delete_report(report_id):
        """
        删除报表（软删除）
        
        Args:
            report_id: 报表ID
            
        Raises:
            404: 如果报表不存在
        """
        report = Report.query.get_or_404(report_id)
        # 软删除，只将is_active设为False
        report.is_active = False
        db.session.commit()
        
    @staticmethod
    def hard_delete_report(report_id):
        """
        硬删除报表（从数据库中删除）
        
        Args:
            report_id: 报表ID
            
        Raises:
            404: 如果报表不存在
        """
        report = Report.query.get_or_404(report_id)
        db.session.delete(report)
        db.session.commit() 