from secrets import choice
from string import ascii_uppercase, digits, ascii_lowercase


def id_generator(size: int = 27) -> str:
    return ''.join(choice(ascii_uppercase + digits + ascii_lowercase) for _ in range(size))
