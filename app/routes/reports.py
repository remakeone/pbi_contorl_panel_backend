from flask import Blueprint, jsonify, request
from app.services.report_service import ReportService
from flask_login import login_required
from app.utils.decorators import permission_required

# 创建报表蓝图
reports = Blueprint('reports', __name__)

@reports.route('/api/reports', methods=['GET'])
@permission_required('view_reports')
def get_reports():
    """
    获取所有报表列表
    
    Returns:
        JSON: 报表列表
    """
    all_reports = ReportService.get_all_reports()
    return jsonify([report for report in all_reports])

@reports.route('/api/reports/<int:report_id>', methods=['GET'])
@permission_required(resource_type='report')
def get_report(report_id):
    """
    获取特定报表详情
    
    Args:
        report_id: 报表ID
        
    Returns:
        JSON: 报表详情
    """
    report = ReportService.get_report_by_id(report_id)
    return jsonify(report.to_dict(need_pbi_id=True))

@reports.route('/api/reports', methods=['POST'])
@permission_required(resource_type='report')
def create_report():
    """
    创建新报表
    
    Returns:
        JSON: 创建的报表信息
    """
    try:
        data = request.get_json()
        report = ReportService.create_report(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 403
    return jsonify(report.to_dict()), 201


@reports.route('/api/reports/<int:report_id>', methods=['POST'])
@permission_required(resource_type='report')
def update_report(report_id):
    """
    更新报表信息
    
    Args:
        report_id: 报表ID
        
    Returns:
        JSON: 更新后的报表信息
    """
    data = request.get_json()
    report = ReportService.update_report(report_id, data)
    return jsonify(report.to_dict())

@reports.route('/api/reports/<int:report_id>', methods=['DELETE'])
@permission_required('edit_reports')
def delete_report(report_id):
    """
    删除报表
    
    Args:
        report_id: 报表ID
        
    Returns:
        空响应，状态码204
    """
    ReportService.delete_report(report_id)
    return '', 204 