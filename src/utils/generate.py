import secrets
import string

alphabet = string.ascii_letters


async def generate_unique_id(length=10):
    return ''.join(secrets.choice(alphabet) for _ in range(length))