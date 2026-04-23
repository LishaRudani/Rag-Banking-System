import uuid
import time

# ✅ global storage
TOKENS = {}

def generate_token():
    token = str(uuid.uuid4())
    expiry = time.time() + 60

    TOKENS[token] = expiry

    print("Generated token:", token)
    print("Stored tokens after generation:", TOKENS)

    return token


def validate_token(token):
    print("Validating token:", token)
    print("Current TOKENS:", TOKENS)

    if token in TOKENS:
        if TOKENS[token] > time.time():
            return True
        else:
            print("Token expired")
            del TOKENS[token]  # cleanup
            return False

    print("Token not found")
    return False