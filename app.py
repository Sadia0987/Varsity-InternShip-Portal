import os
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from sqlalchemy import inspect, text
from models import db, User, Internship, Application 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  

# File Upload Configuration for Profile Picture / CV / Cover Photo
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Safely handle UPLOAD_FOLDER creation
if os.path.exists(UPLOAD_FOLDER):
    if not os.path.isdir(UPLOAD_FOLDER):
        os.remove(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
else:
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///internship.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail Server Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'sabihasharkerpiya.id1530.nub.cse@gmail.com'     
app.config['MAIL_PASSWORD'] = 'ssmt xzvu oitz qhtl'       
app.config['MAIL_DEFAULT_SENDER'] = 'sabihasharkerpiya.id1530.nub.cse@gmail.com'

db.init_app(app)
mail = Mail(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create DB Tables and Automatically Add Missing Columns to existing SQLite DB
with app.app_context():
    db.create_all()
    
    inspector = inspect(db.engine)
    
    # Check User Table Columns
    if 'user' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('user')]
        
        with db.engine.connect() as conn:
            if 'whatsapp_no' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN whatsapp_no VARCHAR(50)"))
            if 'job_duration' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN job_duration VARCHAR(100)"))
            if 'previous_companies' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN previous_companies TEXT"))
            if 'profile_pic' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN profile_pic VARCHAR(255)"))
            if 'cover_photo' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN cover_photo VARCHAR(255)"))
                
            if 'cgpa' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN cgpa VARCHAR(20)"))
            if 'semester' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN semester VARCHAR(50)"))
            if 'skills' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN skills TEXT"))
            if 'bio' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN bio TEXT"))
            if 'github_url' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN github_url VARCHAR(255)"))
            if 'linkedin_url' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN linkedin_url VARCHAR(255)"))
            if 'portfolio_url' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN portfolio_url VARCHAR(255)"))
            if 'resume' not in columns:
                conn.execute(text("ALTER TABLE user ADD COLUMN resume VARCHAR(255)"))
                
            conn.commit()

    # Check Internship Table Columns (Automatically add stipend column)
    if 'internships' in inspector.get_table_names():
        intern_columns = [col['name'] for col in inspector.get_columns('internships')]
        with db.engine.connect() as conn:
            if 'stipend' not in intern_columns:
                conn.execute(text("ALTER TABLE internships ADD COLUMN stipend VARCHAR(100)"))
            conn.commit()

# --- Routes ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/internships')
def internships():
    if not session.get('logged_in'):
        flash("Please login as a student to view internships!")
        return redirect(url_for('login'))
    
    internships_list = Internship.query.all()
    return render_template('internships.html', internships=internships_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            session['logged_in'] = True
            session['user_id'] = user.id
            session['user_name'] = user.fullname
            session['user_type'] = user.role
            flash("Login successful!")
            
            if user.role == 'company':
                return redirect(url_for('company'))
            elif user.role == 'student':
                return redirect(url_for('student'))
            elif user.role == 'alumni':
                return redirect(url_for('alumni'))
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password. Please try again.")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        student_id = request.form.get('student_id')
        department = request.form.get('department')
        
        company_name = request.form.get('company_name')
        designation = request.form.get('designation')
        passing_year = request.form.get('passing_year')
        
        if email and password:
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Email already exists! Try another one.")
                return redirect(url_for('register'))
            
            if role == 'student' and student_id:
                existing_sid = User.query.filter_by(student_id=student_id).first()
                if existing_sid:
                    flash("This Student ID is already registered! Please use your own ID.")
                    return redirect(url_for('register'))
            
            if role == 'student':
                new_user = User(
                    fullname=fullname,
                    email=email,
                    password=password,
                    role='student',
                    student_id=student_id,
                    department=department
                )
            elif role == 'company':
                new_user = User(
                    fullname=fullname,
                    email=email,
                    password=password,
                    role='company'
                )
            elif role == 'alumni':
                new_user = User(
                    fullname=fullname,
                    email=email,
                    password=password,
                    role='alumni',
                    company_name=company_name,
                    designation=designation,
                    passing_year=passing_year
                )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash("Account created successfully! Please sign in.")
            return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/student')
def student():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        flash("Please login as a Student to access this page!")
        return redirect(url_for('login'))
    
    session['user'] = session.get('user_name')
    user_id = session.get('user_id')
    
    current_user = User.query.get(user_id)
    internships_list = Internship.query.all()
    
    my_applications = Application.query.filter_by(student_id=user_id).all()
    applied_job_ids = [app.internship_id for app in my_applications]
    
    total_applied = len(my_applications)
    pending_count = sum(1 for app in my_applications if app.status == 'pending')
    shortlisted_count = sum(1 for app in my_applications if app.status == 'accepted')
    rejected_count = sum(1 for app in my_applications if app.status == 'rejected')

    return render_template(
        'student.html',
        current_user=current_user,
        internships=internships_list,
        my_applications=my_applications,
        applied_job_ids=applied_job_ids,
        total_applied=total_applied,
        pending_count=pending_count,
        shortlisted_count=shortlisted_count,
        rejected_count=rejected_count
    )

@app.route('/update-student-profile', methods=['POST'])
def update_student_profile():
    if not session.get('logged_in') or session.get('user_type') != 'student':
        flash("Unauthorized action!")
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        user.cgpa = request.form.get('cgpa')
        user.semester = request.form.get('semester')
        user.skills = request.form.get('skills')
        user.bio = request.form.get('bio')
        user.github_url = request.form.get('github_url')
        user.linkedin_url = request.form.get('linkedin_url')
        user.portfolio_url = request.form.get('portfolio_url')

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"student_pic_{user.id}_{int(datetime.now().timestamp())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_pic = filename

        if 'cover_photo' in request.files:
            file = request.files['cover_photo']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"cover_{user.id}_{int(datetime.now().timestamp())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.cover_photo = filename

        if 'resume' in request.files:
            file = request.files['resume']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"resume_{user.id}_{int(datetime.now().timestamp())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.resume = filename

        try:
            db.session.commit()
            flash("Student profile updated successfully!")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating profile.")
            print("Student Profile Update Error:", e)

    return redirect(url_for('student'))

@app.route('/apply/<int:internship_id>')
def apply_internship(internship_id):
    if not session.get('logged_in') or session.get('user_type') != 'student':
        flash("Please login as a student to apply!")
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    existing_app = Application.query.filter_by(student_id=user_id, internship_id=internship_id).first()

    if existing_app:
        flash("You have already applied for this internship!")
    else:
        new_app = Application(
            student_id=user_id,
            internship_id=internship_id,
            status='pending'
        )
        db.session.add(new_app)
        db.session.commit()
        flash("Applied successfully!")

    return redirect(url_for('student'))

# --- Company Dashboard Route ---
@app.route('/company')
def company():
    if not session.get('logged_in') or session.get('user_type') != 'company':
        flash("Please login as a Company to access this page!")
        return redirect(url_for('login'))

    company_id = session.get('user_id')
    current_company = User.query.get(company_id)
    
    posted_internships = Internship.query.filter_by(company_id=company_id).all()
    applications_list = Application.query.join(Internship).filter(Internship.company_id == company_id).all()
    
    total_posted = len(posted_internships)
    total_applications = len(applications_list)
    pending_count = sum(1 for app in applications_list if app.status == 'pending')
    shortlisted_count = sum(1 for app in applications_list if app.status == 'accepted')

    return render_template(
        'company.html', 
        current_company=current_company, 
        internships=posted_internships,
        applications=applications_list,
        total_posted=total_posted,
        total_applications=total_applications,
        pending_count=pending_count,
        shortlisted_count=shortlisted_count
    )

# --- Application Status Update Route (New Added) ---
@app.route('/update-application-status/<int:app_id>/<string:status>')
def update_application_status(app_id, status):
    if not session.get('logged_in') or session.get('user_type') != 'company':
        flash("Unauthorized action!")
        return redirect(url_for('login'))

    application = Application.query.get(app_id)
    if application and status in ['accepted', 'rejected', 'pending']:
        application.status = status
        db.session.commit()
        flash(f"Application marked as {status}!")

    return redirect(url_for('company'))

# --- Post New Internship Route ---
@app.route('/post-internship', methods=['GET', 'POST'])
def post_internship():
    if not session.get('logged_in') or session.get('user_type') != 'company':
        flash("Please login as a company to post an internship!")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        location = request.form.get('location')
        stipend = request.form.get('stipend')
        deadline_raw = request.form.get('deadline')
        
        deadline_val = None
        if deadline_raw:
            try:
                deadline_val = datetime.strptime(deadline_raw, '%Y-%m-%d').date()
            except ValueError:
                deadline_val = None

        company_id = session.get('user_id')

        try:
            new_internship = Internship(
                title=title,
                description=description,
                location=location,
                stipend=stipend,
                deadline=deadline_val,
                company_id=company_id
            )
            
            db.session.add(new_internship)
            db.session.commit()
            
            flash("Internship posted successfully!")
            return redirect(url_for('company'))
        except Exception as e:
            db.session.rollback()
            flash("Failed to post internship. Please try again.")
            print("Post Internship Error:", e)

    return redirect(url_for('company'))

@app.route('/alumni')
def alumni():
    if not session.get('logged_in'):
        flash("Please login as a Alumni to access this page!")
        return redirect(url_for('login'))

    alumni_list = User.query.filter_by(role='alumni').all()
    current_user = User.query.get(session.get('user_id'))
    return render_template('alumni.html', alumni_list=alumni_list, current_user=current_user)

@app.route('/update-alumni-profile', methods=['POST'])
def update_alumni_profile():
    if not session.get('logged_in') or session.get('user_type') != 'alumni':
        flash("Unauthorized action!")
        return redirect(url_for('alumni'))

    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if user:
        user.company_name = request.form.get('company_name')
        user.designation = request.form.get('designation')
        user.passing_year = request.form.get('passing_year')
        user.whatsapp_no = request.form.get('whatsapp_no')
        user.job_duration = request.form.get('job_duration')
        user.previous_companies = request.form.get('previous_companies')
        user.blood_group = request.form.get('blood_group')

        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(f"alumni_{user.id}_{int(datetime.now().timestamp())}_{file.filename}")
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.profile_pic = filename

        try:
            db.session.commit()
            flash("Profile updated successfully!")
        except Exception as e:
            db.session.rollback()
            flash("An error occurred while updating profile.")
            print("Update Error:", e)

    return redirect(url_for('alumni'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message_body = request.form.get('message')
        sender_name = session.get('user_name', 'Guest User')
        sender_role = session.get('user_type', 'Visitor')

        msg = Message(
            subject=f"[Portal Support] {subject}",
            recipients=['cse@varsity.edu.bd']
        )
        msg.body = f"From: {sender_name} ({sender_role})\nSubject: {subject}\n\nMessage:\n{message_body}"

        try:
            mail.send(msg)
            flash("Your message has been sent successfully to the department desk!")
        except Exception as e:
            flash("Message submitted successfully!")
            print("Mail Send Error:", e)

        return redirect(url_for('contact'))

    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.clear()   
    return redirect(url_for('home')) 

# --- Password Reset Routes ---

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            otp = random.randint(100000, 999999)
            session['reset_email'] = email
            session['otp'] = otp
            session['otp_expiry'] = (datetime.now() + timedelta(minutes=1)).timestamp()

            msg = Message('Password Reset OTP', recipients=[email])
            msg.body = f"Hello {user.fullname},\n\nYour OTP for resetting password is: {otp}\n\nThis code will expire in 1 minute."
            
            try:
                mail.send(msg)
                flash("An OTP has been sent to your email address!")
                return redirect(url_for('verify_otp'))
            except Exception as e:
                flash("Failed to send email. Check mail setup or password.")
                print("Mail Error:", e)
        else:
            flash("No account found with that email address.")

    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        expiry_timestamp = session.get('otp_expiry', 0)

        if datetime.now().timestamp() > expiry_timestamp:
            flash("OTP has expired! Please click Resend OTP.")
            return redirect(url_for('verify_otp'))

        if user_otp and int(user_otp) == session.get('otp'):
            flash("OTP verified! Please set a new password.")
            return redirect(url_for('reset_password'))
        else:
            flash("Invalid OTP! Please try again.")

    return render_template('verify_otp.html')

@app.route('/resend-otp')
def resend_otp():
    email = session.get('reset_email')
    if not email:
        return redirect(url_for('forgot_password'))

    user = User.query.filter_by(email=email).first()
    if user:
        otp = random.randint(100000, 999999)
        session['otp'] = otp
        session['otp_expiry'] = (datetime.now() + timedelta(minutes=1)).timestamp()

        msg = Message('Resend Password Reset OTP', recipients=[email])
        msg.body = f"Hello {user.fullname},\n\nYour new OTP is: {otp}\n\nThis code will expire in 1 minute."
        
        try:
            mail.send(msg)
            flash("A new OTP has been sent to your email!")
        except Exception as e:
            flash("Failed to resend OTP.")
            print("Mail Error:", e)

    return redirect(url_for('verify_otp'))

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        email = session.get('reset_email')

        user = User.query.filter_by(email=email).first()
        if user:
            user.password = new_password
            db.session.commit()

            session.pop('reset_email', None)
            session.pop('otp', None)
            session.pop('otp_expiry', None)

            flash("Password reset successfully! Please log in.")
            return redirect(url_for('login'))

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
