import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import sys

AUTH0_DOMAIN = 'dev-br-wgpeo.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagency'

# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    headers = request.headers.get('Authorization', None)
    if not headers:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Missing Authorization header.'
        }, 401)
    header_parts = headers.split()
    if len(header_parts) == 1 or len(header_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Invalid Authorization header.'
        }, 401)
    if header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header missing Bearer'
        }, 401)
    token = header_parts[1]
    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'forbidden',
            'description': 'Permission not found'
        }, 403)
    return True


def get_rsa_key(token):
    try:
        jwks_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = json.loads(jwks_url.read())
        header = jwt.get_unverified_header(token)
        rsa_key = {}
        if 'kid' not in header:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Authorization malformed.'
            }, 401)
        for key in jwks['keys']:
            if key['kid'] == header['kid']:
                rsa_key = {
                    'kty': key['kty'],
                    'kid': key['kid'],
                    'use': key['use'],
                    'n': key['n'],
                    'e': key['e']
                }
        if not rsa_key:
            raise AuthError({
                'code': 'invalid_key',
                'description': 'Unable to find the appropriate key.'
            }, 401)
        return rsa_key
    except Exception:
        print(sys.exc_info())
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to verify token header.'
        }, 401)


def verify_decode_jwt(token):
    rsa_key = get_rsa_key(token)
    print(rsa_key)
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            print(permission)
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
