import os
import hmac
import time
import base64
import random
import string
import hashlib
import requests
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

URL = "https://audiomack.com/ayrastarr/song/ms-paper-6783918" # put audiomack song url here

def main():
    session = requests.Session()
    song_req = session.get(URL)
    soup = BeautifulSoup(song_req.text, "html.parser")
    song_id = soup.find("span", id=lambda id: id and id.startswith("am-labs-player")).get("id").split("am-labs-player")[1]
    audiomack_api_url = f"https://api.audiomack.com/v1/music/play/{song_id}"
    output_dir = Path("downloads")
    output_dir.mkdir(parents=True, exist_ok=True)
    song = urllib.parse.urlparse(URL).path
    params = {
        "environment": "desktop-web",
        "oauth_consumer_key": "audiomack-web",
        "hq": "true",
        "oauth_nonce": "".join(random.choice(string.ascii_letters + string.digits) for _ in range(32)),
        "oauth_signature_method": "HMAC-SHA1",
        "oauth_timestamp": str(int(time.time())),
        "oauth_version": "1.0",
        "section": song
    }
    signature = generate_signature(params, audiomack_api_url)
    params["oauth_signature"] = signature
    response = session.get(audiomack_api_url, params=params).json()
    audio_url = response["signedUrl"]
    extension = os.path.splitext(urllib.parse.urlparse(audio_url).path)[1]
    audio_response = session.get(audio_url).content
    filename = song.replace("/", " ").strip().replace(" ", "_") + extension
    output_file = output_dir / filename
    with open(output_file, "wb") as f:
        f.write(audio_response)
    print(f"Downloaded music to {output_file}")

def generate_signature(params: dict, audiomack_api_url: str) -> str:
    consumer_secret = "bd8a07e9f23fbe9d808646b730f89b8e" # from audiomack js config code file
    encoded_params = {urllib.parse.quote(k, safe=''): urllib.parse.quote(v, safe='') for k, v in params.items()}
    sorted_params = sorted(encoded_params.items())
    param_string = "&".join([f"{k}={v}" for k, v in sorted_params])
    base_string = "&".join(["GET", urllib.parse.quote(audiomack_api_url, safe=''), urllib.parse.quote(param_string, safe='')])
    signing_key = urllib.parse.quote(consumer_secret, safe='') + '&'
    key_bytes = signing_key.encode('utf-8')
    data_bytes = base_string.encode('utf-8')
    hmac_hash = hmac.new(key_bytes, data_bytes, hashlib.sha1)
    signature_bytes = hmac_hash.digest()
    return base64.b64encode(signature_bytes).decode('utf-8')

if __name__ == "__main__":
    main()