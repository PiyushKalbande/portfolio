from flask import Flask, render_template, request, flash, redirect, url_for
from dotenv import load_dotenv
import gspread
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

gc = gspread.service_account(filename="service.json")
G_KEY = os.getenv('GOOGLE_SHEET_KEY') 
sh = gc.open_by_key(G_KEY)
worksheet = sh.sheet1

# Get social media links from environment
SOCIAL_LINKS = {
    'github': os.getenv('SOCIAL_GITHUB', '#'),
    'instagram': os.getenv('SOCIAL_INSTAGRAM', '#'),
    'linkedin': os.getenv('SOCIAL_LINKEDIN', '#'),
    'facebook': os.getenv('SOCIAL_FACEBOOK', '#')
}

# Email configuration
SOURCE_EMAIL = os.getenv('SOURCE_EMAIL')
DESTINATION_EMAIL = os.getenv('DESTINATION_EMAIL')
MY_PERSONAL_EMAIL= os.getenv('MY_PERSONAL_EMAIL')
EMAIL_APP_PASSWORD = os.getenv('EMAIL_APP_PASSWORD')

with open('Project_Config.json', 'r') as f:
    project_json = json.load(f)
    PROJECTS = project_json.get('projects', [])
    AWARDS = project_json.get('awards', [])
    PORTFOLIO = project_json.get('portfolio', [])
    skills = project_json.get('skills', [])

@app.route("/")
def index():
    """Render the portfolio landing page."""
    return render_template(
        "index.html",
        social_links=SOCIAL_LINKS,
        destination_email=DESTINATION_EMAIL,
        personal_email=MY_PERSONAL_EMAIL,
        projects=PROJECTS,
        award=AWARDS,
        portfolio= PORTFOLIO,
        skills=skills
    )


@app.route("/contact", methods=["POST"])
def contact():
    """Handle contact form submission and send email."""
    try:
        # Get form data
        name = request.form.get('full-name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validate required fields
        if not all([name, email, subject, message]):
            flash('Please fill in all fields.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Validate email format
        if '@' not in email:
            flash('Please enter a valid email address.', 'error')
            return redirect(url_for('index') + '#contact')
        
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = SOURCE_EMAIL
        msg['To'] = DESTINATION_EMAIL
        msg['Subject'] = f"Portfolio Contact: {subject}"
        
        # Create email body
        body = f"""
        New contact form submission from your portfolio website:
        
        Name: {name}
        Email: {email}
        Subject: {subject}
        
        Message:
        {message}
        
        ---
        This email was sent from your portfolio contact form.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email using Gmail SMTP
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(SOURCE_EMAIL, EMAIL_APP_PASSWORD.replace(' ', ''))
            text = msg.as_string()
            server.sendmail(SOURCE_EMAIL, DESTINATION_EMAIL, text)
            server.quit()
            
            try:
                worksheet.append_row([name, email,subject, message])
            except Exception as e:
                print(f"Error has occurd at database side Please try later")
            
            flash('Thank you! Your message has been sent successfully.', 'success')
        except smtplib.SMTPException as e:
            app.logger.error(f"SMTP error: {str(e)}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
        except Exception as e:
            app.logger.error(f"Email error: {str(e)}")
            flash('Sorry, there was an error sending your message. Please try again later.', 'error')
        


    except Exception as e:
        app.logger.error(f"Contact form error: {str(e)}")
        flash('Sorry, there was an error processing your request. Please try again later.', 'error')


    
    
    return redirect(url_for('index') + '#contact')


if __name__ == "__main__":
    app.run()
