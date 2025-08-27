import random
import string

def generate_password(length=16):
    if length < 8:
        raise ValueError("Password minimal 8 karakter.")

    # Karakter yang digunakan
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    # Pastikan password mengandung semua jenis karakter
    password = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(symbols)
    ]

    # Sisa karakter diisi secara acak
    all_chars = lower + upper + digits + symbols
    password += random.choices(all_chars, k=length - 4)

    # Acak urutan karakter
    random.shuffle(password)
    return ''.join(password)

# Contoh penggunaan
print(generate_password(16))