import hashlib
import json
import os
import sys
import difflib
STORE_FILE = "filehashesname.json"
SNAPSHOT_DIR = "file_snapshots"
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
def snapshot_path_for(path):
    safe_name = path.replace(os.sep, "_").replace("/", "_")
    return os.path.join(SNAPSHOT_DIR, safe_name + ".snapshot")
def read_lines(path):
    with open(path, "r", errors="replace") as f:
        return f.readlines()
def save_snapshot(path, lines):
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    with open(snapshot_path_for(path), "w") as f:
        f.writelines(lines)
def load_snapshot(path):
    snap_path = snapshot_path_for(path)
    if os.path.exists(snap_path):
        with open(snap_path, "r", errors="replace") as f:
            return f.readlines()
    return None
def show_diff(old_lines , new_lines , path):
    for i in range(len(new_lines)):
        if old_lines[i] != new_lines[i]:
            print(f"In the line {i+1} changed occured")
            print(f"before the change : {old_lines[i]}")
            print(f"after the change : {new_lines[i]}")
def check_file(path):
    store = load_store()
    current_hash = sha256_of_file(path)
    old_hash = store.get(path)
    current_lines = read_lines(path)
    if old_hash is None:
        print(f"[NEW] {path} -> {current_hash}")
    elif old_hash != current_hash:
        print(f"changed: {path}")
        old_lines = load_snapshot(path)
        if old_lines is not None:
            print("--- diff ---")
            show_diff(old_lines, current_lines, path)
        else:
            print("(no previous snapshot found to diff against)")
    else:
        print(f"[UNCHANGED] {path}")
    # Update stored hash and snapshot for next run
    store[path] = current_hash
    save_store(store)
    save_snapshot(path, current_lines)
if __name__ == "__main__":
    check_file("Data/x.txt")
    