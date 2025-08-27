import itertools
import string
import os
from tqdm import tqdm  # Pastikan sudah install: pip install tqdm

def estimate_combinations(characters, min_len, max_len):
    total = 0
    for length in range(min_len, max_len + 1):
        total += len(characters) ** length
    return total

def generate_wordlist(characters, min_len, max_len, filename, limit=None):
    total_combos = estimate_combinations(characters, min_len, max_len)
    if limit and limit < total_combos:
        total_combos = limit

    with open(filename, "w") as file:
        counter = 0
        with tqdm(total=total_combos, desc="Generating", unit="words") as pbar:
            for length in range(min_len, max_len + 1):
                for combo in itertools.product(characters, repeat=length):
                    file.write("".join(combo) + "\n")
                    counter += 1
                    pbar.update(1)
                    if limit and counter >= limit:
                        return
    print(f"[INFO] Wordlist berhasil disimpan ke: {filename}")

def main():
    print("=== Advanced Wordlist Generator ===")
    print("Pilih karakter:")
    print("(1) huruf kecil")
    print("(2) huruf besar")
    print("(3) huruf kecil + huruf besar")
    print("(4) huruf + angka")
    print("(5) huruf + angka + simbol")
    print("(6) custom karakter")

    pilihan = input("Masukkan pilihan (1-6): ")

    if pilihan == "1":
        chars = string.ascii_lowercase
    elif pilihan == "2":
        chars = string.ascii_uppercase
    elif pilihan == "3":
        chars = string.ascii_letters
    elif pilihan == "4":
        chars = string.ascii_letters + string.digits
    elif pilihan == "5":
        chars = string.ascii_letters + string.digits + string.punctuation
    elif pilihan == "6":
        chars = input("Masukkan karakter custom: ")
    else:
        print("[ERROR] Pilihan tidak valid!")
        return

    try:
        min_len = int(input("Panjang minimum: "))
        max_len = int(input("Panjang maksimum: "))
        if min_len <= 0 or max_len < min_len:
            print("[ERROR] Panjang tidak valid!")
            return
    except ValueError:
        print("[ERROR] Input panjang harus angka!")
        return

    filename = input("Nama file output (contoh: wordlist.txt): ").strip()
    if filename == "":
        filename = "wordlist.txt"

    limit_input = input("Batas jumlah kata (Enter jika tanpa batas): ")
    limit = int(limit_input) if limit_input.strip() else None

    # Estimasi sebelum generate
    total_combos = estimate_combinations(chars, min_len, max_len)
    print(f"[INFO] Estimasi total kombinasi: {total_combos}")
    if limit:
        print(f"[INFO] Akan dibatasi menjadi {limit} kata")

    confirm = input("Lanjutkan? (y/n): ").lower()
    if confirm != "y":
        print("[INFO] Dibatalkan.")
        return

    generate_wordlist(chars, min_len, max_len, filename, limit)

if __name__ == "__main__":
    main()
