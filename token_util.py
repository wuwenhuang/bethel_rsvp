import os
from itsdangerous import URLSafeSerializer

def _serializer() -> URLSafeSerializer:
    secret = os.environ["SIGNING_SECRET"]
    return URLSafeSerializer(secret_key=secret, salt="rsvp-emailer-v1")

def make_token(payload: dict) -> str:
    return _serializer().dumps(payload)

def read_token(token: str) -> dict:
    return _serializer().loads(token)
