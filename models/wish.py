from datetime import datetime
from models.database import db

class WishLike(db.Model):
    __tablename__ = 'wish_likes'

    id = db.Column(db.Integer, primary_key=True)
    wish_id = db.Column(db.Integer, db.ForeignKey('wishes.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class Wish(db.Model):
    __tablename__ = 'wishes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    author = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='wishes')
    likes_rel = db.relationship('WishLike', backref='wish', lazy='dynamic', cascade='all, delete-orphan')

    def to_dict(self, current_user_id=None, client_ip=None):
        liked = False
        if current_user_id:
            liked = WishLike.query.filter_by(wish_id=self.id, user_id=current_user_id).first() is not None
        elif client_ip:
            liked = WishLike.query.filter_by(wish_id=self.id, ip_address=client_ip).first() is not None

        return {
            "id": self.id,
            "user_id": self.user_id,
            "author": self.author,
            "role": self.role or "Amigo Dev",
            "message": self.message,
            "timestamp": self.timestamp.strftime("%d/%m/%Y %H:%M"),
            "likes": self.likes,
            "is_liked": liked
        }
