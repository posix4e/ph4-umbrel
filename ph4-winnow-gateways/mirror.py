"""The census mirror for Winnow's I2P gateway.

Serves /srv on port 8480, to i2pd's server tunnel and to the status page, and
keeps /srv/census/peers.json and peers.json.sig copied from the public census.
As in winnowwallet/census gateways/i2p-mirror/winnow-census-sync, the files are
copied together with size and time limits and the list is only checked to
parse: the wallet verifies the signature, so the mirror is never trusted.
"""

import functools
import http.server
import json
import os
import random
import tempfile
import threading
import time
import urllib.request

ROOT = "/srv"
CENSUS = os.path.join(ROOT, "census")
BASE = "https://census.winnowwallet.com/census"
# The census host refuses Python's default User-Agent.
HEADERS = {"User-Agent": "winnow-census-mirror/1.0"}
# name: (largest accepted body in bytes, timeout in seconds)
LIMITS = {"peers.json": (4_194_304, 120), "peers.json.sig": (65_536, 60)}


def fetch(name, directory):
    limit, timeout = LIMITS[name]
    request = urllib.request.Request(f"{BASE}/{name}", headers=HEADERS)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read(limit + 1)
    if len(body) > limit:
        raise ValueError(f"{name} is over {limit} bytes")
    path = os.path.join(directory, name)
    with open(path, "wb") as file:
        file.write(body)
    os.chmod(path, 0o644)
    return path


def sync():
    os.makedirs(CENSUS, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT) as tmp:
        peers = fetch("peers.json", tmp)
        signature = fetch("peers.json.sig", tmp)
        with open(peers, "rb") as file:
            json.load(file)
        # The list just before its signature, as the guest script does. A fetch
        # between the two can pair a new list with the old signature; the
        # wallet rejects that pair and retries.
        os.replace(peers, os.path.join(CENSUS, "peers.json"))
        os.replace(signature, os.path.join(CENSUS, "peers.json.sig"))


def keep_synced():
    time.sleep(60)
    while True:
        try:
            sync()
        except Exception as error:  # a failed pass leaves the last good pair
            print(f"census sync failed: {error}", flush=True)
        time.sleep(1800 + random.uniform(0, 120))


threading.Thread(target=keep_synced, daemon=True).start()
handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
http.server.ThreadingHTTPServer(("0.0.0.0", 8480), handler).serve_forever()
