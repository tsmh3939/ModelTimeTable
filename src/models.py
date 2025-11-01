from datetime import datetime
from src import db


class User(db.Model):
    """ユーザーモデル（サンプル）"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'


# 他のモデルをここに追加できます
# 例:
# class Post(db.Model):
#     __tablename__ = 'posts'
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#
#     user = db.relationship('User', backref=db.backref('posts', lazy=True))
#
#     def __repr__(self):
#         return f'<Post {self.title}>'