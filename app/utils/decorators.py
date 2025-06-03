from functools import wraps
from flask import jsonify
from flask_login import current_user
from flask import request
from app.services.report_service import ReportService  # 添加服务类导入

def permission_required(resource_type):
    """
    权限检查装饰器
    用于检查用户是否具有特定权限
    
    Args:
        permission (str): 需要检查的权限名称
        
    Returns:
        function: 装饰器函数
        
    Example:
        @permission_required('view_reports')
        def view_report():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查用户是否已登录
            if not current_user.is_authenticated:
                return jsonify({'error': '请先登录'}), 401
            # 管理员绕过检查
            if current_user.role == 'admin':
                return f(*args, **kwargs)
            # 检查用户是否具有所需权限
            # 资源型权限检查（如报表访问）
            if resource_type == 'report':
                report_id = kwargs.get('report_id') or request.json.get('report_id')
                if not current_user.can_view_report(ReportService.get_report_by_id(report_id)):
                    return jsonify({'error': '无该报表访问权限'}), 403
            elif resource_type == 'manage_groups':
                if current_user.role != 'admin':
                    return jsonify({'error': '非管理员无法访问角色组'}), 403
            # 传统权限检查
            elif not current_user.has_permission(resource_type):
                return jsonify({'error': '权限不足'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator 