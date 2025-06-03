import json
import re
import requests
from app import db
from app.models.user import User
from datetime import datetime
from sqlalchemy import or_
from app.services.user_service import UserService
from config import Config


class DingtalkAuthService:

    @staticmethod
    def remove_english_characters(input_string):
        """
        从输入字符串中剔除英文字符。

        Args:
            input_string (str): 输入的字符串。

        Returns:
            str: 剔除英文字符后的字符串。
        """
        return re.sub(r'[a-zA-Z]', '', input_string)

    @staticmethod
    def get_user_token(code):
        """获取用户token"""
        url = "https://api.dingtalk.com/v1.0/oauth2/userAccessToken"
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            "clientSecret": Config.DINGTALK_APP_SECRET,
            "clientId": Config.DINGTALK_APP_KEY,
            "code": code,
            "grantType": "authorization_code",
            "refreshToken": "1"
        }
        response = requests.post(url,headers=headers, data=json.dumps(data))
        if "accessToken" in response.json():
            return response.json()
        else:
            raise Exception("获取用户token失败")

    @staticmethod
    def get_user_info(code):
        """获取用户信息"""
        # 1. 获取用户token
        print(code)
        user_token = DingtalkAuthService.get_user_token(code)
        url = "https://api.dingtalk.com/v1.0/contact/users/me"
        headers = {
            'Content-Type': 'application/json',
            'x-acs-dingtalk-access-token': user_token["accessToken"]
        }
        response = requests.get(url,headers=headers)
        print(response.json())
        return response.json()

    @staticmethod
    def login_or_create_user(dingtalk_info):
        """登录或创建用户（支持预注册用户绑定）"""
        # 首先尝试用钉钉ID查找已注册用户
        username = dingtalk_info.get('nick', dingtalk_info.get('name'))
        if dingtalk_info.get('unionId') is None:
            user = None
        else:
            user = User.query.filter_by(dingtalk_id=dingtalk_info['unionId']).first()

        if not user:
            # 获取用户名（使用钉钉返回的昵称）
            chinese_username = DingtalkAuthService.remove_english_characters(username)
            # 查找预注册用户（同名且未绑定钉钉的用户）
            pre_registered_user = User.query.filter(
                or_(User.name == username, User.name == chinese_username),
                or_(User.dingtalk_id == username, User.dingtalk_id == chinese_username)
            ).first()

            if pre_registered_user: # 如果找到预注册用户，则绑定钉钉账号，否则创建新用户
                # 绑定钉钉账号到预注册用户
                pre_registered_user.dingtalk_id = dingtalk_info['unionId']
                # 把用户名修正为钉钉全名
                if pre_registered_user.name != username:
                    pre_registered_user.name = username
                user = pre_registered_user
            else:
                # 创建全新用户
                dink_id = dingtalk_info.get("unionId",dingtalk_info.get("dingtalk_id"))
                if not dink_id:
                    dink_id = username
                user = User(
                    dingtalk_id=dink_id,
                    name=username,
                    email=dingtalk_info.get('email', '')
                )
                db.session.add(user)
                user_id = User.query.filter_by(dingtalk_id=dink_id).first()
                UserService.add_user_to_role_groups(user_id.id, dingtalk_info.get('role_group_ids', []))
        else:
            # 更新用户信息（如果需要）
            if user.name != username:
                user.name = username
        # 更新最后登录时间（无论新老用户都更新）
        user.last_login = datetime.utcnow()
        db.session.commit()
        return user
