from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import gspread
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import threading
import traceback

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Safe private key handling
private_key = os.getenv("GOOGLE_PRIVATE_KEY")
if not private_key:
    raise RuntimeError("GOOGLE_PRIVATE_KEY not set in environment!")
private_key = private_key.replace("\\n", "\n")

service_info = {
    "type": "service_account",
    "project_id": os.getenv("GOOGLE_PROJECT_ID", ""),
    "private_key_id": os.getenv("GOOGLE_PRIVATE_KEY_ID", ""),
    "private_key": private_key,
    "client_email": os.getenv("GOOGLE_CLIENT_EMAIL", ""),
    "client_id": os.getenv("GOOGLE_CLIENT_ID", ""),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('GOOGLE_CLIENT_EMAIL','')}"
}

gc = gspread.service_account_from_dict(service_info)
G_KEY = os.getenv('GOOGLE_SHEET_KEY')
sh = gc.open_by_key(G_KEY)
worksheet = sh.sheet1

# Social links
SOCIAL_LINKS = {
    'github': os.getenv('SOCIAL_GITHUB', '#'),
    'instagram': os.getenv('SOCIAL_INSTAGRAM', '#'),
    'linkedin': os.getenv('SOCIAL_LINKEDIN', '#'),
    'facebook': os.getenv('SOCIAL_FACEBOOK', '#')
}

# Email config
SOURCE_EMAIL = os.getenv('SOURCE_EMAIL')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL')
EMAIL_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')
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
        destination_email=DESTINATION_EMAIL,
        personal_email=MY_PERSONAL_EMAIL,
        projects=PROJECTS,
        award=AWARDS,
        portfolio=PORTFOLIO,
        skills=skills
    )

def send_email_and_log(name, email, subject, message):
    """Background task: send email + log to sheet"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SOURCE_EMAIL
        msg['To'] = DESTINATION_EMAIL
        msg['Subject'] = f"Portfolio Contact: {subject}"

        body = f"""
        New contact form submission:

        Name: {name}
        Email: {email}
        Subject: {subject}

        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=20)
        server.starttls()
        server.login(SOURCE_EMAIL, EMAIL_APP_PASSWORD.strip())
        server.sendmail(SOURCE_EMAIL, DESTINATION_EMAIL, msg.as_string())
        server.quit()

        worksheet.append_row([name, email, subject, message])
    except Exception as e:
        app.logger.error(f"Background task error: {e}\n{traceback.format_exc()}")

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

        # ✅ Immediate response
        flash('Thanks! Your message is being processed.', 'success')
        response = redirect(url_for('index') + '#contact')

        # ✅ Background thread for heavy work
        threading.Thread(target=send_email_and_log, args=(name, email, subject, message)).start()

        return response

    except Exception as e:
        app.logger.error(f"Contact form error: {e}\n{traceback.format_exc()}")
        flash('Sorry, there was an error processing your request.', 'error')
        return redirect(url_for('index') + '#contact')

if __name__ == "__main__":
    app.run()
