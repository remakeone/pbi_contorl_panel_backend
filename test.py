#!/usr/bin/env python
# -*- coding: utf-8 -*-
# time: 2023/10/11 10:19
# file: login_manager.py
# author: 孙伟亮
# email: 2849068933@qq.com
import time
import json
import requests

from alibabacloud_dingtalk.oauth2_1_0.client import Client as dingtalkoauth2_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.oauth2_1_0 import models as dingtalkoauth_2__1__0_models
from alibabacloud_dingtalk.contact_1_0.client import Client as dingtalkcontact_1_0Client
from alibabacloud_dingtalk.contact_1_0 import models as dingtalkcontact__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
from core.constant import CONSTANT
from core.access_token_manager import AccessTokenManager
from utils.db_tool import save_to_db
from utils.flask_app import config
access_token_manager = AccessTokenManager()


class GetUserInfo:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkcontact_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkcontact_1_0Client(config)

    @staticmethod
    def get_user_info(
            access_token,
    ):
        client = GetUserInfo.create_client()
        get_user_headers = dingtalkcontact__1__0_models.GetUserHeaders()
        get_user_headers.x_acs_dingtalk_access_token = access_token
        try:
            return client.get_user_with_options("me", get_user_headers, util_models.RuntimeOptions())
        except Exception as err:
            print(err.message)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                return {}
            return {}


class GetUserToken:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkoauth2_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkoauth2_1_0Client(config)

    @staticmethod
    def get_user_token(
            code,
    ):
        client = GetUserToken.create_client()
        get_user_token_request = dingtalkoauth_2__1__0_models.GetUserTokenRequest(
            client_id=config.get("AppKey"),
            client_secret=config.get("AppSecret"),
            code=code,
            refresh_token='abcd',
            grant_type='authorization_code'
        )
        try:
            return client.get_user_token(get_user_token_request)
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                return {}
            return {}


def check_user_login_state(uuid):
    if uuid in CONSTANT.LOGIN_USERS:
        if time.time() - CONSTANT.LOGIN_USERS.get(uuid, {}).get("login_time", 0) < 3600 * 24 * 7:
            return True
    return False


def getbyunionid(unionid):
    try:
        url = f"https://oapi.dingtalk.com/topapi/user/getbyunionid?access_token={access_token_manager.access_token}"

        payload = json.dumps({"unionid": unionid})
        headers = {
            'Content-Type': 'text/plain'
        }

        response = requests.request("POST", url, headers=headers, data=payload).json()
        if response.get("errcode", -1) == 0:
            return True, "登陆成功"
        return False, "登陆失败"
    except:
        return False, "服务器错误"


def login_dd(uuid, code):
    user_accessToken = GetUserToken.get_user_token(code=code)
    print(user_accessToken)
    if user_accessToken:
        accessToken = user_accessToken.to_map().get("body", {}).get("accessToken", None)
        print(accessToken)
        if accessToken:
            user_info = GetUserInfo.get_user_info(access_token=accessToken)
            if user_info:
                unionId = user_info.to_map().get("body", {}).get("unionId", None)
                if unionId:
                    success, msg = getbyunionid(unionId)
                    if success:
                        CONSTANT.LOGIN_USERS[uuid] = user_info.to_map().get("body")
                        CONSTANT.LOGIN_USERS[uuid]["login_time"] = time.time()
                        save_to_db(CONSTANT.LOGIN_USERS[uuid].get("nick",""),"login")
                    return msg
        return "获取用户信息失败"
    return "获取用户user_accessToken失败"


