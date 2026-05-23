from app.extensions import db, bcrypt, login_manager
from datetime import datetime
from flask_login import UserMixin
import enum

class TaskStatus(enum.Enum):
    PENDING = "pending"
    # enum.name = enum.value
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# User Table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)

    username = db.Column(db.String(100), nullable=False, unique=True)

    email = db.Column(db.String(100), nullable=False, unique=True, index=True)

    password = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    tasks = db.relationship("Task", backref="user",lazy=True)

    def __init__(self, username, email, password):
        self.username = username 
        self.email = email 
        self.create_password(password)

    def create_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode("utf-8")

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)
    




# Task Table
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100), nullable=False)

    description = db.Column(db.Text, nullable=True)

    time_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=True) #Changable by users

    status = db.Column(db.Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)


@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))