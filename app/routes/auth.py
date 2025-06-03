from flask import Blueprint, jsonify, request
from flask_login import login_user, logout_user, login_required, current_user
from app.services.auth_service import DingtalkAuthService
from urllib.parse import urlencode
from config import Config
from loguru import logger

# 创建认证蓝图
auth = Blueprint('auth', __name__)

@auth.route('/api/auth/dingtalk/url', methods=['GET'])
def get_dingtalk_url():
    """
    获取钉钉登录二维码URL
    用于前端展示钉钉登录二维码
    Returns:
        dict: 包含登录URL的JSON响应
    """
    url = f"https://oapi.dingtalk.com/connect/qrconnect"
    params = {
        "appid": Config.DINGTALK_APP_KEY,
        "response_type": "code",
        "scope": "snsapi_login",
        "redirect_uri": Config.DINGTALK_REDIRECT_URI,
    }
    return jsonify({"url": url + "?" + urlencode(params)})

@auth.route('/api/auth/dingtalk/callback', methods=['POST'])
def dingtalk_callback():
    """
    处理钉钉登录回调
    接收钉钉授权码，获取用户信息并完成登录
    Returns:
        dict: 包含登录结果的JSON响应
    """
    # 获取授权码
    code = request.json.get('code')
    if not code:
        return jsonify({'error': '无效的请求'}), 400

    try:
        # 获取用户信息
        user_info = DingtalkAuthService.get_user_info(code)
        if 'error' in user_info:
            return jsonify({'error': user_info['errmsg']}), 400

        # 登录或创建用户
        user = DingtalkAuthService.login_or_create_user(user_info)
        login_user(user)

        return jsonify({
            'message': '登录成功',
            'user': user.to_dict()
        })
    except Exception as e:
        logger.error(f"钉钉登录失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """
    用户登出接口
    清除用户会话
    Returns:
        dict: 包含登出结果的JSON响应
    """
    logout_user()
    return jsonify({'message': '登出成功'})

@auth.route('/api/auth/user', methods=['GET'])
@login_required
def get_current_user():
    """
    获取当前登录用户信息
    Returns:
        dict: 包含用户信息的JSON响应
    """
    return jsonify(current_user.to_dict())


