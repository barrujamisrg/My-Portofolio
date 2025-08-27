import requests
import concurrent.futures
from tqdm import tqdm
import sys

# Pastikan user memberikan file input
if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} urls.txt")
    sys.exit(1)

input_file = sys.argv[1]

# Baca daftar URL
with open(input_file, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

alive_sites = []

def check_url(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return url
    except:
        return None
    return None

print(f"[INFO] Checking {len(urls)} URLs...")

# Multi-thread + Progress Bar
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = list(tqdm(executor.map(check_url, urls), total=len(urls), desc="Checking"))

# Filter hasil OK
for res in results:
    if res:
        alive_sites.append(res)

# Simpan ke file
if alive_sites:
    with open("alive_sites.txt", "w") as f:
        f.write("\n".join(alive_sites))
    print(f"[DONE] {len(alive_sites)} sites alive. Saved to alive_sites.txt")
else:
    print("[INFO] No alive sites found.")
