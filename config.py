import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Config:
    """
    应用配置类
    包含所有应用配置项，从环境变量中读取
    """
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 't')
    
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/pbi_control')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG
    
    # CORS配置
    CORS_HEADERS = 'Content-Type'
    
    # 钉钉配置
    DINGTALK_APP_KEY = os.getenv('DINGTALK_APP_KEY', '')
    DINGTALK_APP_SECRET = os.getenv('DINGTALK_APP_SECRET', '')
    DINGTALK_REDIRECT_URI = os.getenv('DINGTALK_REDIRECT_URI', 'http://localhost:5000/api/auth/dingtalk/callback')
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Power BI配置
    POWERBI_BASE_URL = os.getenv('POWERBI_BASE_URL', 'https://app.powerbi.com/view')

    SESSION_COOKIE_SAMESITE='None'
    # SESSION_COOKIE_SECURE=True  # 如果使用 HTTPS

class DevelopmentConfig(Config):
    """
    开发环境配置
    """
    DEBUG = True
    SQLALCHEMY_ECHO = False
    # 开发环境覆盖生产安全设置
    SESSION_COOKIE_SECURE = False  # 允许HTTP使用SameSite=None
    SESSION_COOKIE_SAMESITE = 'Lax'  # 降级SameSite策略（可选方案）

class TestingConfig(Config):
    """
    测试环境配置
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/pbi_control_test')
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """
    生产环境配置
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False
    # 确保在生产环境中使用强密钥
    SECRET_KEY = os.getenv('SECRET_KEY') or None
    if not SECRET_KEY:
        raise ValueError("未设置SECRET_KEY环境变量，这在生产环境中是必须的")


# 配置映射
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

# 根据FLASK_ENV环境变量选择配置
def get_config():
    """
    获取当前环境对应的配置
    根据FLASK_ENV环境变量选择配置类
    返回配置类
    """
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, config_by_name['default']) 