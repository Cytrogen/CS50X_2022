import math
import random
from hashlib import md5
from flask import redirect, session, current_app, url_for
from functools import wraps
from itsdangerous import URLSafeTimedSerializer


def login_required(f):
    """
    Decorate routes to require login
    """
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def OTP_generator():
    digits = "0123456789"
    OTP = ""
    for i in range(6):
        OTP += digits[math.floor(random.random() * 10)]
    return int(OTP)


# Encode the Email address and a timestamp in a token
def encode_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')


# Decode the token and returns the email address as long as the token is not older than an hour
def decode_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token,
                                 salt='email-confirm-salt',
                                 max_age=expiration)
        return email
    except Exception:
        return False
    
    
# Take an endpoint and an encoded token and then returns a unique URL
def generate_url(endpoint, token):
    return url_for(endpoint,
                   token=token,
                   _external=True)
    
    
# Generate hash for email address for avatar generating
def hash_email(email):
    hash = md5(email.lower().encode('utf-8')).hexdigest()
    return hash