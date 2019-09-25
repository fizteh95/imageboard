from datetime import datetime
# from hashlib import md5
from app import db  # , login
import json
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash


# followers = db.Table(
#     'followers',
#     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
#     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
# )


# class User(db.Model):  # UserMixin,
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     posts = db.relationship('Post', backref='author', lazy='dynamic')
#     about_me = db.Column(db.String(140))
#     last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    # followed = db.relationship(
    #     'User', secondary=followers,
    #     primaryjoin=(followers.c.follower_id == id),
    #     secondaryjoin=(followers.c.followed_id == id),
    #     backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

#     def __repr__(self):
#         return '<User {}>'.format(self.username)

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    # def avatar(self, size):
    #     digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    #     return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
    #         digest, size)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         self.followed.append(user)

    # def unfollow(self, user):
    #     if self.is_following(user):
    #         self.followed.remove(user)

    # def is_following(self, user):
    #     return self.followed.filter(
    #         followers.c.followed_id == user.id).count() > 0

    # def followed_posts(self):
    #     followed = Post.query.join(
    #         followers, (followers.c.followed_id == Post.user_id)).filter(
    #             followers.c.follower_id == self.id)
    #     own = Post.query.filter_by(user_id=self.id)
    #     return followed.union(own).order_by(Post.timestamp.desc())


# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))


# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(140))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)


# answers = db.Table('answers',
#                      db.Column('answ_from_id', db.Integer, db.ForeignKey('post.id')),
#                      db.Column('answ_to_id', db.Integer, db.ForeignKey('post.id')) )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OP_num = db.Column(db.Integer, index=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    OP_flag = db.Column(db.Integer)
    image_ref = db.Column(db.String(120))
    board_name = db.Column(db.String(10), db.ForeignKey('board.ref'))
    answers = db.Column(db.String(100))
    # или просто сериализируем
    #_ratings = Column(db.String, default='0.0')
    @property
    def _answers(self):
        return [0, 1]
        # if type(self.answers) == str:
        #     return json.loads(self.answers)
        # else:
        #     return [0, 1]
    @_answers.setter
    def _answers(self, value):
        self.answers = json.dumps(value)
    
    # reply = db.relationship(
    #     'Post', secondary=answers,
    #     primaryjoin=(answers.c.answ_from_id == id),
    #     secondaryjoin=(answers.c.answ_to_id == id),
    #     backref=db.backref('answers', lazy='dynamic'), lazy='dynamic')
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)





    # post.answ_from_id.all()
    # post1.answ_from_id.append(user2)
    # post1.answ_from_id.remove(user2)
    # пример сложного запроса на объединение
#     def followed_posts(self):
#         return Post.query.join(
#             followers, (followers.c.followed_id == Post.user_id)).filter(
#                 followers.c.follower_id == self.id).order_by(
#                     Post.timestamp.desc())
    
class Board(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ref = db.Column(db.String(100), unique=True)
    post_rel = db.relationship('Post', backref='board', lazy='dynamic')
    description = db.Column(db.String(100))

    def __repr__(self):
        return '<Board {}>'.format(self.ref)


# class Answers(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     answer_from = db.Column(db.Integer, index=True)
#     answer_to = db.Column(db.Integer, index=True)
#     ###
#     post_rel = db.relationship('Post', backref='rep_from', lazy='dynamic')
#     post_rel = db.relationship('Post', backref='rep_to', lazy='dynamic')

#     def __repr__(self):
#         return '<Board {}>'.format(self.ref)
