from sqlalchemy import func, ForeignKey
from applications.database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    
    # Define relationship to Journal
    journals = db.relationship('Journal', back_populates='user', cascade="all, delete-orphan")


class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    
    # Foreign key to link each journal to a specific user
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    
    # Define the relationship back to User
    user = db.relationship('User', back_populates='journals')
