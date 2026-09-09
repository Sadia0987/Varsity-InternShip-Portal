from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. Main User Table (Student, Company & Alumni)
class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False) 
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'student', 'company', 'alumni'
    
    # Student Info
    student_id = db.Column(db.String(50), unique=True, nullable=True) 
    department = db.Column(db.String(100), nullable=True)
    cgpa = db.Column(db.String(20), nullable=True)
    semester = db.Column(db.String(50), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    portfolio_url = db.Column(db.String(255), nullable=True)
    resume = db.Column(db.String(255), nullable=True)       # Resume PDF filename
    
    # Alumni Specific Info
    company_name = db.Column(db.String(150), nullable=True)
    designation = db.Column(db.String(150), nullable=True)
    passing_year = db.Column(db.String(50), nullable=True)  # Batch Number
    job_duration = db.Column(db.String(100), nullable=True)
    previous_companies = db.Column(db.Text, nullable=True)
    blood_group = db.Column(db.String(10), nullable=True)
    whatsapp_no = db.Column(db.String(50), nullable=True)
    
    # Profile Pictures
    profile_pic = db.Column(db.String(255), nullable=True)
    cover_photo = db.Column(db.String(255), nullable=True)
    
    # Company Specific Details
    website = db.Column(db.String(150), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posted_internships = db.relationship('Internship', backref='company', cascade="all, delete-orphan", lazy=True)
    applications = db.relationship('Application', backref='student', cascade="all, delete-orphan", lazy=True)


# 2. Internship Post Table
class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    stipend = db.Column(db.String(100), nullable=True)
    deadline = db.Column(db.Date, nullable=True)
    status = db.Column(db.String(20), default='active')  # 'active', 'closed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='internship', cascade="all, delete-orphan", lazy=True)

    # Template Helper Properties
    @property
    def company_name(self):
        return self.company.company_name or self.company.fullname if self.company else "Partner Company"

    @property
    def posted_date(self):
        return self.created_at.strftime('%d %b, %Y') if self.created_at else "Recently"


# 3. Student Application Table
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    status = db.Column(db.String(20), default='pending')  # 'pending', 'accepted', 'rejected'
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
