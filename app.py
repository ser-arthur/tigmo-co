from flask import Flask, render_template, request, jsonify
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/contact', methods=['POST'])
def contact():
    # Get form data
    name = request.form.get('name')
    company = request.form.get('company')
    email = request.form.get('email')
    message = request.form.get('message')
    subject = request.form.get('subject', f"New Contact Form Submission from {name}")

    SENDER_EMAIL = os.environ.get('MAIL_USERNAME')
    SENDER_PASSWORD = os.environ.get('MAIL_PASSWORD')
    RECIPIENT_EMAIL = os.environ.get('MAIL_RECIPIENT')

    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL]):
        print("ERROR: Mail server credentials are not configured in environment variables.")
        return jsonify({'success': False, 'message': 'Server configuration error. Could not send message.'})

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    # Email body
    body = f"""
    You have a new message from the TIGMO website contact form:

    Name: {name}
    Company: {company}
    Email: {email}

    Message:
    {message}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.zoho.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Send the email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        server.quit()

        print(f"Successfully sent email from {name} ({email})")
        return jsonify({'success': True, 'message': 'Message sent successfully!'})

    except Exception as e:
        print(f"ERROR: Failed to send email. Error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred while sending the message.'})

if __name__ == '__main__':
    app.run(debug=True)