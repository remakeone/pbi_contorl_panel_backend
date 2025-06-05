from app import db


class Tag(db.Model):
    """
    标签模型类
    存储报表标签信息
    """
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())