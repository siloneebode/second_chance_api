import random


def generate_otp_code():
    digits = "0123456789"
    code = ""
    for _ in range(6):
        code += digits[random.randint(0, 9)]
    return code
