# Varsity Internship Portal

> A centralized web-based internship platform connecting university
> students, companies, and alumni through internship opportunities,
> applications, professional profiles, and career networking.

## 👥 Team Members

-   **Sabiha Sharker Piya**
-   **Sadia Afrin**
-   **Md Al Amin**

## 📌 Project Overview

**Varsity Internship Portal (VIP)** is a full-stack web application
designed to reduce the gap between university students and the
technology industry.

The platform provides a structured environment where students can
discover and apply for internships, companies can publish internship
opportunities and manage applications, and alumni can build professional
profiles and connect with students.

The system also supports profile management, CV and image uploads,
application status tracking, and role-based access.

## ✨ Key Features

### 👨‍🎓 Student Features

-   Student registration and login
-   Student-specific dashboard
-   Personal profile management
-   Academic information management
-   Skills and bio management
-   GitHub, LinkedIn, and portfolio links
-   Profile picture and cover photo upload
-   Resume/CV PDF upload
-   Browse available internships
-   Apply for internships
-   Prevention of duplicate applications
-   Track internship application status

### 🏢 Company Features

-   Company registration and login
-   Company-specific dashboard
-   Company profile information
-   Post internship opportunities
-   Add internship description, category, location, stipend, and
    deadline
-   Manage posted internships
-   View received applications
-   Track total and pending applications
-   Shortlist/accept or reject applicants
-   Manage application status

### 🎓 Alumni Networking

-   Dedicated alumni section
-   Alumni professional profiles
-   Company and designation information
-   Graduation/batch information
-   Job duration and previous company information
-   WhatsApp/contact information
-   Alumni search/filter functionality
-   Alumni profile editing
-   Direct connection option through WhatsApp

### 🔐 Authentication & Access Control

-   Role-based registration
-   Login/logout functionality
-   Separate access for students, companies, and alumni
-   Session-based user authentication
-   Role-specific navigation and dashboards
-   Forgot-password interface and email-based functionality

### 🌐 General Portal Features

-   Responsive user interface
-   Home page with featured internship opportunities
-   Internship listing page
-   About section
-   Contact and faculty information
-   Flash messages for user actions and validation
-   Responsive navigation bar
-   Modern dark-themed UI
-   Font Awesome icons
-   Portal logo and favicon

## 🛠️ Technology Stack

### Frontend

-   HTML5
-   CSS3
-   JavaScript
-   Tailwind CSS
-   Font Awesome

### Backend

-   Python
-   Flask
-   Flask-Mail

### Database

-   SQLite
-   Flask-SQLAlchemy
-   SQLAlchemy

### Development & Collaboration

-   Git
-   GitHub
-   GitHub Forks, Branches and Pull Requests

## 🏗️ System Architecture

``` text
                    Varsity Internship Portal
                              |
                +-------------+-------------+
                |             |             |
             Student       Company        Alumni
                |             |             |
          +-----+-----+   +---+---+    +---+---+
          |           |   |       |    |       |
       Profile    Apply  Post    Manage Profile Connect
          |           |   |       |
          +-----------+---+-------+
                      |
                   Database
                      |
                   SQLite
```

## 🗄️ Database Design

The application uses SQLAlchemy models to manage users, internships, and
applications.

### User

Stores common and role-specific information for:

-   Students
-   Companies
-   Alumni

Student-related data includes student ID, department, CGPA, semester,
skills, bio, resume, and professional links.

Company-related data includes company name, website, and verification
status.

Alumni-related data includes company, designation, passing year, job
duration, previous companies, blood group, and WhatsApp contact.

### Internship

Stores:

-   Internship title
-   Description
-   Category
-   Location
-   Stipend
-   Application deadline
-   Status
-   Company relationship
-   Creation date

### Application

Stores:

-   Student
-   Internship
-   Application status
-   Application date

Supported application states include:

-   Pending
-   Accepted
-   Rejected

## 🔄 Main User Workflow

### Student

``` text
Register
   ↓
Login
   ↓
Complete Profile
   ↓
Browse Internships
   ↓
Apply
   ↓
Track Application Status
```

### Company

``` text
Register
   ↓
Login
   ↓
Company Dashboard
   ↓
Post Internship
   ↓
Receive Applications
   ↓
Review Applicants
   ↓
Accept / Reject / Keep Pending
```

### Alumni

``` text
Register
   ↓
Login
   ↓
Create Professional Profile
   ↓
Browse Alumni Network
   ↓
Search / Filter Alumni
   ↓
Connect
```

## 📂 Project Structure

``` text
Varsity-Internship-Portal/
│
├── app.py
├── models.py
├── internship.db
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student.html
│   ├── company.html
│   ├── internships.html
│   ├── alumni.html
│   └── contact.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── main.js
│   │
│   ├── Images/
│   │   └── Logo.png
│   │
│   └── uploads/
│
└── README.md
```

> The exact file/folder list may vary depending on the latest project
> version.

## ⚙️ Installation & Setup

### 1. Clone the repository

``` bash
git clone <repository-url>
cd Varsity-Internship-Portal
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

Activate it on Windows:

``` bash
venv\Scripts\activate
```

On macOS/Linux:

``` bash
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install flask flask-sqlalchemy flask-mail werkzeug
```

If a `requirements.txt` file is included in the repository, use:

``` bash
pip install -r requirements.txt
```

### 4. Configure email credentials

The application uses Flask-Mail for email functionality.

For security, email credentials should be stored using environment
variables or a local configuration file that is **not committed to
GitHub**.

Example:

``` text
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
```

Never publish real passwords, API keys, or other secrets in the
repository.

### 5. Run the application

``` bash
python app.py
```

Then open the local Flask URL shown in the terminal, commonly:

``` text
http://127.0.0.1:5000/
```

## 🔒 Security Note

Before making the repository public, remove any real credentials or
secrets from source code and rotate any credential that may already have
been exposed.

Use environment variables for:

-   Secret keys
-   Email passwords/app passwords
-   API keys
-   Other private credentials

## 🤝 GitHub Collaboration

This project was developed as a three-member team using GitHub for
collaboration.

Recommended workflow:

``` text
Main Repository
      ↓
Fork / Collaborator Access
      ↓
Individual Branch
      ↓
Code Changes
      ↓
Commit
      ↓
Push
      ↓
Pull Request
      ↓
Review
      ↓
Merge
```

### Team Members

  Member                Role
  --------------------- ---------------------------------------
  Sabiha Sharker Piya   Team Member / Contributor
  Sadia Afrin           Team Member / Contributor
  Md Al Amin            Team Member / Repository Collaborator

## 🎯 Project Objectives

-   Create a centralized internship platform for university students
-   Make internship discovery easier
-   Allow companies to publish and manage internship opportunities
-   Simplify the internship application process
-   Provide students with professional profiles and CV management
-   Build an alumni networking platform
-   Implement role-based access and dashboards
-   Demonstrate practical full-stack web development using Flask

## 🚀 Future Improvements

-   Advanced internship search and filtering
-   Email notifications for application status changes
-   Company verification workflow
-   Admin moderation and analytics
-   Faculty recommendation/feedback module
-   Internship bookmarking
-   Automated CV parsing
-   Recommendation system for matching students with internships
-   Cloud database and production deployment
-   Stronger authentication and password hashing
-   Mobile application support

## 📜 License

This project was developed as an academic/team project for educational
purposes.

------------------------------------------------------------------------

**Varsity Internship Portal --- Connecting Students, Companies &
Alumni.**
