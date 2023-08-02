import re

from flask import Flask, render_template, request, redirect, jsonify, abort
import os
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='your-gmail-username',
    MAIL_PASSWORD='your-gmail-password'
)
mail = Mail(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


@app.route('/contact', methods=['POST'])  # Make sure to specify POST here
def contact():
    # Process the form data here
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    message = request.form.get('message')

    # Send email using Flask-Mail
    msg = Message('New Contact Form Submission', recipients=['recipient@example.com'])
    msg.body = f"Full Name: {fullname}\nEmail: {email}\nMessage: {message}"
    try:
        mail.send(msg)
        success = True
    except Exception as e:
        print(e)
        success = False
    return jsonify({'success': success})

@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
