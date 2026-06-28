import hashlib
import json
import os
import sys
import time
STORE_FILE = "filehashesname.json"
def sha256_of_file(path, chunk_size=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            h.update(chunk)
    return h.hexdigest()
def load_store():
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r") as f:
            return json.load(f)
    return {}
def save_store(store):
    with open(STORE_FILE, "w") as f:
        json.dump(store, f, indent=2)
def check_file(path):
    store = load_store()
    current_hash = sha256_of_file(path)
    old_hash = store.get(path)
    if old_hash is None:
        print(f"[NEW] {path} -> {current_hash}")
    elif old_hash != current_hash:
        print(f"changed: {path}")
    else:
        print(f"[UNCHANGED] {path}")
    store[path] = current_hash
    save_store(store)
if __name__ == "__main__":
    check_file("x.txt")