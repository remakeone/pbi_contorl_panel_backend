from flask import Blueprint, request, jsonify
from app import db
from app.models import RoleGroup
from app.utils.decorators import permission_required
from app.services.role_group_service import RoleGroupService

role_groups = Blueprint('role_groups', __name__)


@role_groups.route('/api/role_groups', methods=['GET'])
@permission_required('view_role_groups')
def get_role_groups():
    """
    获取所有角色组列表
    
    Returns:
        JSON: 角色组列表
    """
    all_role_groups = RoleGroupService.get_all_role_groups()
    return jsonify([role_group.to_dict() for role_group in all_role_groups])


@role_groups.route('/api/role_groups/<int:group_id>', methods=['GET'])
@permission_required('view_role_groups')
def get_role_group(group_id):
    """
    获取特定角色组详情
    
    Args:
        group_id: 角色组ID
        
    Returns:
        JSON: 角色组详情
    """
    role_group = RoleGroupService.get_role_group_by_id(group_id)
    return jsonify(role_group.to_dict())


@role_groups.route('/api/role_groups', methods=['POST'])
@permission_required('manage_role_groups')
def create_role_group():
    """
    创建新角色组
    
    Returns:
        JSON: 创建的角色组信息
    """
    data = request.get_json()
    role_group = RoleGroupService.create_role_group(data)
    return jsonify(role_group.to_dict()), 201


@role_groups.route('/api/role_groups/<int:group_id>', methods=['PUT'])
@permission_required('manage_role_groups')
def update_role_group(group_id):
    """
    更新角色组信息
    
    Args:
        group_id: 角色组ID
        
    Returns:
        JSON: 更新后的角色组信息
    """
    data = request.get_json()
    role_group = RoleGroupService.update_role_group(group_id, data)
    return jsonify(role_group.to_dict())


@role_groups.route('/api/role_groups/<int:group_id>', methods=['DELETE'])
@permission_required('manage_role_groups')
def delete_role_group(group_id):
    """
    删除角色组
    
    Args:
        group_id: 角色组ID
        
    Returns:
        空响应，状态码204
    """
    RoleGroupService.delete_role_group(group_id)
    return '', 204


@role_groups.route('/api/role_groups/<int:group_id>/users', methods=['GET'])
@permission_required('view_role_groups')
def get_group_users(group_id):
    """
    获取角色组下的所有用户
    
    Args:
        group_id: 角色组ID
        
    Returns:
        JSON: 用户列表
    """
    users = RoleGroupService.get_group_users(group_id)
    return jsonify([user.to_dict() for user in users])


@role_groups.route('/api/role_groups/<int:group_id>/users', methods=['POST'])
@permission_required('manage_role_groups')
def add_users_to_group(group_id):
    """
    添加用户到角色组
    
    Args:
        group_id: 角色组ID
        
    Returns:
        JSON: 操作结果
    """
    data = request.get_json()
    user_id = data.get('user_id', [])
    RoleGroupService.add_users_to_group(group_id, [user_id])
    return jsonify({'message': '用户添加成功'})


@role_groups.route('/api/role_groups/<int:group_id>/users/<int:user_id>', methods=['DELETE'])
@permission_required('manage_role_groups')
def remove_user_from_group(group_id, user_id):
    """
    从角色组中移除用户
    
    Args:
        group_id: 角色组ID
        user_id: 用户ID
        
    Returns:
        空响应，状态码204
    """
    RoleGroupService.remove_user_from_group(group_id, user_id)
    return '', 204


@role_groups.route('/api/role_groups/<int:group_id>/visible_reports', methods=['GET'])
@permission_required('view_role_groups')
def get_group_visible_reports(group_id):
    """
    获取角色组的可见报表列表

    Args:
        group_id: 角色组ID

    Returns:
        JSON: 可见报表列表
    """
    reports = RoleGroupService.get_group_visible_reports(group_id)
    return jsonify([report.to_dict() for report in reports])


@role_groups.route('/api/role_groups/<int:group_id>/visible_reports', methods=['POST'])
@permission_required('manage_role_groups')
def set_group_visible_reports(group_id):
    """
    设置角色组的可见报表

    Args:
        group_id: 角色组ID

    Returns:
        JSON: 操作结果
    """
    data = request.get_json()
    report_ids = data.get('report_ids', [])
    RoleGroupService.set_group_visible_reports(group_id, report_ids)
    return jsonify({'message': '可见报表设置成功'})


@role_groups.route('/api/role_groups/<int:group_id>/visible_reports/<int:report_id>', methods=['POST'])
@permission_required('manage_role_groups')
def add_visible_report_to_group(group_id, report_id):
    """
    添加单个报表到角色组的可见报表

    Args:
        group_id: 角色组ID
        report_id: 报表ID

    Returns:
        JSON: 操作结果
    """
    RoleGroupService.add_reports_to_group(group_id, [report_id])
    return jsonify({'message': '报表添加成功'})


@role_groups.route('/api/role_groups/<int:group_id>/visible_reports/<int:report_id>', methods=['DELETE'])
@permission_required('manage_role_groups')
def remove_visible_report_from_group(group_id, report_id):
    """
    从角色组的可见报表中移除单个报表

    Args:
        group_id: 角色组ID
        report_id: 报表ID

    Returns:
        空响应，状态码204
    """
    RoleGroupService.remove_report_from_group(group_id, report_id)
    return '', 204
