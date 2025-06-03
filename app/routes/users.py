from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from app.utils.decorators import permission_required
from app.services.user_service import UserService
from app.services.auth_service import DingtalkAuthService

users = Blueprint('users', __name__)

@users.route('/api/users', methods=['GET'])
@permission_required('view_users')
def get_users():
    """
    获取所有用户列表
    
    Returns:
        JSON: 用户列表
    """
    all_users = UserService.get_all_users()
    return jsonify([user.to_dict() for user in all_users])


@users.route('/api/users/<int:user_id>', methods=['GET'])
@permission_required('view_users')
def get_user(user_id):
    """
    获取特定用户详情
    
    Args:
        user_id: 用户ID
        
    Returns:
        JSON: 用户详情
    """
    user = UserService.get_user_by_id(user_id)
    return jsonify(user.to_dict())

@users.route('/api/users', methods=['POST'])
@permission_required('manage_users')
def create_user():
    """
    创建新用户
    
    Returns:
        JSON: 创建的用户信息
    """
    data = request.get_json()
    user = DingtalkAuthService.login_or_create_user(data)
    return jsonify(user.to_dict()), 201

@users.route('/api/users/<int:user_id>', methods=['PUT'])
@permission_required('manage_users')
def update_user(user_id):
    """
    更新用户信息
    
    Args:
        user_id: 用户ID
        
    Returns:
        JSON: 更新后的用户信息
    """
    data = request.get_json()
    user = UserService.update_user(user_id, data)
    return jsonify(user.to_dict())


@users.route('/api/users/<int:user_id>', methods=['DELETE'])
@permission_required('manage_users')
def delete_user(user_id):
    """
    删除用户
    
    Args:
        user_id: 用户ID
        
    Returns:
        空响应，状态码204
    """
    UserService.delete_user(user_id)
    return '', 204

@users.route('/api/users/<int:user_id>/role-groups', methods=['GET'])
@permission_required('view_users')
def get_user_role_groups(user_id):
    """
    获取用户所属的所有角色组
    
    Args:
        user_id: 用户ID
        
    Returns:
        JSON: 角色组列表
    """
    role_groups = UserService.get_user_role_groups(user_id)
    return jsonify([role_group.to_dict() for role_group in role_groups])

@users.route('/api/users/<int:user_id>/role-groups', methods=['POST'])
@permission_required('manage_users')
def add_user_to_role_groups(user_id):
    """
    将用户添加到多个角色组
    
    Args:
        user_id: 用户ID
        
    Returns:
        JSON: 操作结果
    """
    data = request.get_json()
    role_group_ids = data.get('role_group_ids', [])
    UserService.add_user_to_role_groups(user_id, role_group_ids)
    return jsonify({'message': '用户已成功添加到角色组'})

@users.route('/api/users/<int:user_id>/role-groups/<int:role_group_id>', methods=['DELETE'])
@permission_required('manage_users')
def remove_user_from_role_group(user_id, role_group_id):
    """
    将用户从角色组中移除
    
    Args:
        user_id: 用户ID
        role_group_id: 角色组ID
        
    Returns:
        空响应，状态码204
    """
    UserService.remove_user_from_role_group(user_id, role_group_id)
    return '', 204 