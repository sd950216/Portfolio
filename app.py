from flask import Flask, render_template, request, jsonify
import os
from flask_mail import Mail, Message
from flask_caching import Cache

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='motrappentesting@gmail.com',
    MAIL_DEFAULT_SENDER='motrappentesting@gmail.com',
    MAIL_PASSWORD=f'{os.getenv("MAIL_PASSWORD")}',
)
# Configure Flask-Caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

print(f'{os.getenv("MAIL_PASSWORD")}')
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
    msg = Message('New Contact Form Submission', recipients=['meen79508@gmail.com'])
    msg.body = 'This is a plain text version of the email. Please use an email client that supports HTML to view the content.'
    msg.html = email_content  # Set the HTML content
    try:
        mail.send(msg)
        success = True
    except Exception as e:
        print(e)
        success = False

    return jsonify({'success': success})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
