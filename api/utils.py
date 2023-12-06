import random
import string


def generate_flag(length: int = 31) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length)) + "="
