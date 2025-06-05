from app.models.report import Report
from app import create_app, db

# 创建 Flask 应用实例
app = create_app()

# 使用应用上下文
with app.app_context():
    try:
        all_reports = Report.query.all()
        print(all_reports)
    except Exception as e:
        print(f"查询报表时出错: {e}")