import os
import hmac
import time
import base64
import random
import string
import hashlib
import requests
import argparse
import urllib.parse
from pathlib import Path

CONSUMER_SECRET = "bd8a07e9f23fbe9d808646b730f89b8e"
ENDPOINT_URL = "https://api.audiomack.com/v1/music/play/83257322"

def main():
    output_dir = Path("downloads")
    output_dir.mkdir(parents=True, exist_ok=True)
    parser = argparse.ArgumentParser("Download music from Audiomack")
    parser.add_argument("url", type=audiomack_url, help="The URL of the music to download")
    args = parser.parse_args()
    song = urllib.parse.urlparse(args.url).path
    params = {
        "environment": "desktop-web",
        "oauth_consumer_key": "audiomack-web",
        "hq": "true",
        "oauth_nonce": generate_nonce(),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_version": "1.0",
        "section": song
    }
    signature = generate_signature(params)
    params["oauth_signature"] = signature
    response = requests.get(ENDPOINT_URL, params=params).json()
    audio_url = response["signedUrl"]
    extension = os.path.splitext(urllib.parse.urlparse(audio_url).path)[1]
    audio_response = requests.get(audio_url).content
    filename = song.replace("/", " ").strip().replace(" ", "_") + extension
    output_file = output_dir / filename
    with open(output_file, "wb") as f:
        f.write(audio_response)
    print(f"Downloaded music to {output_file}")

def audiomack_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme not in {"http", "https"}:
        raise argparse.ArgumentTypeError("URL must start with http:// or https://")
    if not parsed.netloc:
        raise argparse.ArgumentTypeError("Invalid URL")
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    if domain != "audiomack.com":
        raise argparse.ArgumentTypeError("URL must be from audiomack.com")
    if not parsed.path or parsed.path == "/":
        raise argparse.ArgumentTypeError("Audiomack URL must contain a path")
    return value

def generate_nonce(length: int = 32) -> str:
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def generate_signature(params: dict) -> str:
    encoded_params = {urllib.parse.quote(k, safe=''): urllib.parse.quote(v, safe='') for k, v in params.items()}
    sorted_params = sorted(encoded_params.items())
    param_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    base_string = "&".join(["GET", urllib.parse.quote(ENDPOINT_URL, safe=''), urllib.parse.quote(param_string, safe='')])
    signing_key = urllib.parse.quote(CONSUMER_SECRET, safe='') + '&'
    key_bytes = signing_key.encode('utf-8')
    data_bytes = base_string.encode('utf-8')
    hmac_hash = hmac.new(key_bytes, data_bytes, hashlib.sha1)
    signature_bytes = hmac_hash.digest()
    return base64.b64encode(signature_bytes).decode('utf-8')

if __name__ == "__main__":
    main()