from datetime import datetime, timedelta, date
import secrets
import random
import string


def generate_token(expiry_date, db):
    alphabet = string.ascii_letters  # Get a string containing all the alphabets (both upper and lower case)
    first_char = random.choice(alphabet)  # Randomly choose an alphabet as the first character
    token = "md-" + first_char + secrets.token_hex(60)

    creation_date = date.today().strftime("%Y-%m-%d")

    token_details = {
        "created_at": creation_date,
        "expiry_date" : expiry_date,
        "token" : token 
    }

    db.insert(token_details)

    return token