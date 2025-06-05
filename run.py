from app import create_app, db
from flask_migrate import Migrate
from sqlalchemy.exc import SQLAlchemyError
from loguru import logger
logger.add("app/log.log", rotation="10 MB")
from flask import request
import traceback
app = create_app()

# 初始化数据库迁移
migrate = Migrate(app, db)

# 请求钩子
@app.before_request
def log_request():
    logger.info(f"请求开始 | {request.method} {request.path} | 数据: {request.get_json(silent=True)}")


@app.after_request
def log_response(response):
    logger.info(f"请求完成 | 状态码: {response.status_code}, 响应数据: {response.get_json(silent=True)}")
    return response


@app.route('/')
def index():
    """
    根路由处理函数
    用于健康检查
    """
    return {'status': 'ok', 'message': 'Power BI控制面板后端服务运行正常'}

@app.errorhandler(404)
def not_found_error(error):
    """
    404错误处理
    """

    return {'error': str(error)}, 404


@app.errorhandler(Exception)
def internal_error(error):
    """
    500错误处理
    安全地处理数据库会话回滚
    """
    # 检查db是否已初始化
    if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
        print(error)
        return {'error': str(error)}, 500
        
    try:
        # 检查db和session是否可用
        if db and hasattr(db, 'session'):
            # 检查是否有活动的数据库会话
            if hasattr(db.session, 'is_active') and db.session.is_active:
                db.session.rollback()
    except SQLAlchemyError:
        # 如果数据库操作失败，静默处理
        pass
    except Exception:
        # 其他异常也静默处理，避免递归
        pass
    logger.error(traceback.format_exc())
    return {'error': str(error)}, 500

if __name__ == '__main__':
    # 开发环境配置
    app.run(
        host='0.0.0.0',  # 允许外部访问
        port=4888,       # 默认端口
        debug=False       # 开发模式
    )
