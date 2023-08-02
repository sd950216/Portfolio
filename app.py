import re

from flask import Flask, render_template, request, redirect, jsonify, abort
import os
from flask_mail import Mail, Message
from flask_caching import Cache
import time

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='example@example.com',
    MAIL_DEFAULT_SENDER='example@example.com',
    MAIL_PASSWORD='your_password',
)
# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


# Custom decorator to implement rate limiting
def rate_limit(limit_per, key_func):
    def decorator(func):
        def wrapper(*args, **kwargs):
            key = key_func(*args, **kwargs)
            if cache.get(key):
                return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429  # HTTP 429: Too Many Requests
            else:
                cache.set(key, True, timeout=limit_per)
                return func(*args, **kwargs)

        return wrapper

    return decorator


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


@app.route('/contact', methods=['POST'])
@rate_limit(limit_per=300, key_func=lambda: request.remote_addr)
def contact():
    # Process the form data here
    fullname = request.form.get('fullname')
    email = request.form.get('email')
    message = request.form.get('message')

    # Create HTML-formatted email content
    email_content = f"""
    <html>
        <body>
            <h2>New Contact Form Submission</h2>
            <p><strong>Full Name:</strong> {fullname}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
        </body>
    </html>
    """

    # Send email using Flask-Mail with HTML content
    msg = Message('New Contact Form Submission', recipients=['recipient@example.com'])
    msg.body = 'This is a plain text version of the email. Please use an email client that supports HTML to view the content.'
    msg.html = email_content  # Set the HTML content
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
