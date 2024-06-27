import random
import string

# Generating a random secret key
def generate_secret_key():
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits + '!@#$%^&*(-_=+)') for _ in range(50))

SECRET_KEY = generate_secret_key()
