from app import db

# 多对多关联表
report_tags = db.Table('report_tags',
    db.Column('report_id', db.Integer, db.ForeignKey('reports.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=db.func.current_timestamp())
)