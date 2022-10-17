import jwt
from decouple import config
from datetime import datetime, timedelta

def generate_reset_password_link(user):
    token = jwt.encode(
        {
            "iss": "temp_value",
            "iat": int(datetime.now().timestamp()),
            "exp": int((datetime.now() + timedelta(minutes=15)).timestamp()),
            "unique": user.password
        },
        config('SIGNATURE'),
        'HS256'
    )
    return token

def verify_rest_password_link(token):
    try:
        jwt.decode(
            token,
            config('SIGNATURE'),
            ['HS256'],
            options={
                'verify_signature':True,
                'require': ['iat', 'exp', 'unique'],
                'verify_iss': 'verify_signature',
                'verify_iat': 'verify_signature',
                'verify_exp': 'verify_signature',
            },
            issuer='temp_value'
        )
    except jwt.exceptions.InvalidTokenError:
        return False