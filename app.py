from flask import Flask, render_template, request, flash, redirect, url_for, session
from dotenv import load_dotenv
import os
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define table structure with timestamp
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Social links
SOCIAL_LINKS = {
    'github': os.getenv('SOCIAL_GITHUB', '#'),
    'instagram': os.getenv('SOCIAL_INSTAGRAM', '#'),
    'linkedin': os.getenv('SOCIAL_LINKEDIN', '#'),
    'facebook': os.getenv('SOCIAL_FACEBOOK', '#')
}

MY_PERSONAL_EMAIL = os.getenv('MY_PERSONAL_EMAIL')

# Load project config
with open('Project_Config.json', 'r') as f:
    project_json = json.load(f)
    PROJECTS = project_json.get('projects', [])
    AWARDS = project_json.get('awards', [])
    PORTFOLIO = project_json.get('portfolio', [])
    skills = project_json.get('skills', [])

@app.route("/")
def index():
    return render_template(
        "index.html",
        social_links=SOCIAL_LINKS,
        personal_email=MY_PERSONAL_EMAIL,
        projects=PROJECTS,
        award=AWARDS,
        portfolio=PORTFOLIO,
        skills=skills
    )

@app.route("/contact", methods=["POST"])
def contact():
    try:
        name = request.form.get('full-name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not all([name, email, subject, message]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('index') + '#contact')

        if '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('index') + '#contact')

        new_msg = Message(name=name, email=email, subject=subject, message=message)
        db.session.add(new_msg)
        db.session.commit()

        flash('Thank you! Your message has been saved successfully.', 'success')

    except Exception as e:
        app.logger.error(f"Contact form error: {e}")
        flash('Sorry, there was an error saving your message.', 'error')

    return redirect(url_for('index') + '#contact')

# ✅ Admin login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == os.getenv("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True
            return redirect(url_for("admin"))
        else:
            flash("Invalid password", "error")
            return redirect(url_for("login"))
    return render_template("login.html")

# ✅ Admin page (protected)
@app.route("/admin")
def admin():
    if not session.get("admin_logged_in"):
        flash("Please log in to access admin page", "error")
        return redirect(url_for("login"))

    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template(
        "admin.html",
        messages=messages,
        projects=PROJECTS,
        awards=AWARDS,
        portfolio=PORTFOLIO,
        skills=skills,
        social_links=SOCIAL_LINKS,
        personal_email=MY_PERSONAL_EMAIL
    )

# ✅ Logout route
@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    flash("Logged out successfully", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
