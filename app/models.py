from xml.etree.ElementTree import Comment
from . import db,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    pass_secure = db.Column(db.String(255))
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
  
    @property
    def password(self):
        raise AttributeError('You cannnot access this attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def __repr__(self):
        return f'User {self.username}'
    
    
class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    blog_id = db.Column(db.Integer,db.ForeignKey('blogs.id'),nullable = False)
    comment = db.Column(db.String)
    posted = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey("users.id"))
    
    def save(self,):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,blog_id):
        comments = Comments.query.filter_by(blog_id=blog_id).all()
        return comments
    
    def __repr__(self):
        return f'Comment {self.blog_comment}'
class Blogs(db.Model):

    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    blog_text = db.Column(db.String(2000))
    posted = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comments', backref = 'blogs', lazy='dynamic')
    
    def save_b(self):
        db.session.add(self)
        db.session.commit()

  
  
class Quote:
    '''
  Quote class to define Quote Objects
    '''

    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(255))
    quote = db.Column(db.String(2000))
    
    def save(self,):
            db.session.add(self)
            db.session.commit()

    @classmethod
    def get_quote(cls,id):
        quote = Quote.query.filter_by(id=id).all()
        return quote
    
    def __repr__(self):
        return f'Comment {self.quote}'
