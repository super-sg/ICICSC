import os
import time
import hashlib
import subprocess
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings()

CACHE_DIR = os.path.join(os.path.dirname(__file__), 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
}

def get_cache_path(url: str) -> str:
    h = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{h}.html")

def fetch_url(url: str, max_retries: int = 3, timeout: int = 15, use_cache: bool = True) -> str:
    cache_path = get_cache_path(url)
    if use_cache and os.path.exists(cache_path) and os.path.getsize(cache_path) > 500:
        with open(cache_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    for attempt in range(1, max_retries + 1):
        try:
            # First try requests
            resp = requests.get(url, headers=HEADERS, verify=False, timeout=timeout)
            if resp.status_code == 200 and len(resp.text) > 200:
                with open(cache_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(resp.text)
                return resp.text
        except Exception:
            pass

        # Fallback to curl
        try:
            cmd = ['curl', '-s', '-L', '-k', '--max-time', str(timeout),
                   '-A', HEADERS['User-Agent'], url]
            out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
            if len(out) > 200:
                with open(cache_path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(out)
                return out
        except Exception:
            pass

        time.sleep(1.5 * attempt)

    return ""

def fetch_soup(url: str, **kwargs) -> BeautifulSoup:
    html = fetch_url(url, **kwargs)
    return BeautifulSoup(html, 'html.parser')
