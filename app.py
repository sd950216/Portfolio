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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')


@app.route('/projects')
def projects():
    return render_template('projects.html')


# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         message = request.form['message']
#
#         msg = Message(
#             subject='New Message from Portfolio',
#             sender=email,
#             recipients=['your-email-address']
#         )
#         msg.body = f"From: {name}\nEmail: {email}\nMessage: {message}"
#         mail.send(msg)
#
#         return redirect('/thank-you')
#     return render_template('contact.html')
def is_valid_email(email):
    """
    Check if an email address is in a valid format using regular expressions.
    """
    # Regular expression to match the email pattern
    pattern = '^[\w]{1,}[\w.+-]{0,}@[\w-]{2,}([.][a-zA-Z]{2,}|[.][\w-]{2,}[.][a-zA-Z]{2,})$'

    # Use re.match() to match the pattern against the email address
    match = re.match(pattern, email)

    # Return True if there is a match, False otherwise
    return bool(match)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    # check if all fields are filled
    if not name or not email or not subject or not message:
        return jsonify({'message': 'error', 'error': 'Please fill out all fields.'})
    # send the message
    # ...
    elif not is_valid_email(email):
        return jsonify({'message': 'error', 'error': 'Please enter a valid email.'})

    print("3rd ", name, email, subject, message)

    return jsonify({'message': 'success', 'success': 'Your message was sent successfully.'})


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
