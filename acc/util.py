import random
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

def generate_random_number(min_value,max_value):
    return random.randint(min_value,max_value)

def send_email_to(email,first_name,last_name):
    otp = generate_random_number(1000,9999)
    subject = "Verify Your Account - OTP Confirmation"
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Account Creation OTP</title>
    <style>
    body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .header {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }}
            .otp-box {{
                font-size: 28px;
                font-weight: bold;
                background: #007bff;
                color: #fff;
                padding: 10px;
                display: inline-block;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .message {{
                font-size: 16px;
                color: #555;
                margin: 15px 0;
            }}
            .footer {{
                font-size: 14px;
                color: #777;
                margin-top: 20px;
            }}
            .support {{
                font-weight: bold;
                color: #007bff;
            }}
    </style>
</head>
<body>

<div class="container">
    <p class="header">Verify Your Email</p>

    <p class="message">Dear <strong> User </strong>, {first_name} {last_name}</p>

    <p class="message">Thank you for signing up with ParkVenue! Use the OTP below to verify your email and activate your account:</p>

    <p class="otp-box">{otp}</p>

    <p class="message">This OTP is valid for the next <strong>10 minutes</strong>. For security reasons, please do not share this code with anyone.</p>

    <p class="message">If you did not sign up, please ignore this email or contact our <span class="support">support team</span> immediately.</p>

    <p class="footer">Best regards,<br>ParkVenue Support Team<br>
    <a href="https://skillnetzpythonanywhere.com">ParkVenuepythonanywhere.com</a></p>
</div>

</body>
</html>
"""

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    
    try:
        email_msg = EmailMessage(subject, html_content, from_email, recipient_list)
        email_msg.content_subtype = "html"  # Set content type to HTML
        email_msg.send()
    except Exception as e:
        print(f"Error sending email: {e}")
    
    return otp

def send_email_reset(email):
    otp = generate_random_number(1000, 9999)
    
    subject = "Reset Your Password - OTP Confirmation"

    # HTML Email Template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Password Reset OTP</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 20px auto;
                background: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .header {{
                font-size: 24px;
                font-weight: bold;
                color: #333;
            }}
            .otp-box {{
                font-size: 28px;
                font-weight: bold;
                background: #007bff;
                color: #fff;
                padding: 10px;
                display: inline-block;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .message {{
                font-size: 16px;
                color: #555;
                margin: 15px 0;
            }}
            .footer {{
                font-size: 14px;
                color: #777;
                margin-top: 20px;
            }}
            .support {{
                font-weight: bold;
                color: #007bff;
            }}
        </style>
    </head>
    <body>

    <div class="container">
        <p class="header">Reset Your Password</p>

        <p class="message">Dear <strong> User </strong>,</p>

        <p class="message">We received a request to reset your password. Use the OTP below to proceed:</p>

        <p class="otp-box">{otp}</p>

        <p class="message">This OTP is valid for the next <strong>10 minutes</strong>. For security reasons, please do not share this code with anyone.</p>

        <p class="message">If you did not request this reset, ignore this email or contact our <span class="support">support team</span> immediately.</p>

        <p class="footer">Best regards,<br>ParkVenue Support Team<br>
        <a href="https://skillnetzpythonanywhere.com">ParkVenuepythonanywhere.com</a></p>
    </div>

    </body>
    </html>
    """

    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        email_msg = EmailMessage(subject, html_content, from_email, recipient_list)
        email_msg.content_subtype = "html"  # Set content type to HTML
        email_msg.send()
    except Exception as e:
        print(f"Error sending email: {e}")

    return otp