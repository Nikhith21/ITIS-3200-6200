import hashlib
import os
import json

HASH_FILE = "hash_table.json"

def normalize_path(p):
    return os.path.normcase(os.path.abspath(p))

def hash_file(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None

def scan_directory(dir_path):
    """
    Returns:
        hash_to_paths: { hash: [path1, path2, ...] }
        path_to_hash:  { path: hash }
    """
    hash_to_paths = {}
    path_to_hash = {}

    for root, dirs, files in os.walk(dir_path):
        for name in files:
            path = normalize_path(os.path.join(root, name))
            if normalize_path(path) == normalize_path(HASH_FILE):
                continue

            h = hash_file(path)
            if h is None:
                continue

            path_to_hash[path] = h

            if h not in hash_to_paths:
                hash_to_paths[h] = []
            hash_to_paths[h].append(path)

    return hash_to_paths, path_to_hash

def generate_table():
    dir_path = input("Enter the directory path to hash: ").strip()
    if not os.path.isdir(dir_path):
        print("Invalid directory.")
        return

    hash_to_paths, _ = scan_directory(dir_path)

    with open(HASH_FILE, "w") as f:
        json.dump(hash_to_paths, f, indent=4)

    print("Hash table generated.")

def validate_hashes():
    if not os.path.exists(HASH_FILE):
        print("No hash table found. Generate one first.")
        return

    with open(HASH_FILE, "r") as f:
        stored_hash_to_paths = json.load(f)

    # Normalize stored paths
    stored_hash_to_paths = {
        h: [normalize_path(p) for p in paths]
        for h, paths in stored_hash_to_paths.items()
    }

    dir_path = input("Enter the directory path to verify: ").strip()
    if not os.path.isdir(dir_path):
        print("Invalid directory.")
        return

    current_hash_to_paths, current_path_to_hash = scan_directory(dir_path)

    updated_table = {h: list(paths) for h, paths in stored_hash_to_paths.items()}

    matched_current_paths = set()

    for h, old_paths in stored_hash_to_paths.items():
        if h in current_hash_to_paths:
            new_paths = current_hash_to_paths[h]

            for old_path in old_paths:
                if old_path in new_paths:
                    print(f"{old_path}: VALID")
                    matched_current_paths.add(old_path)
                else:
                    candidate = None
                    for p in new_paths:
                        if p not in matched_current_paths:
                            candidate = p
                            break

                    if candidate:
                        print(f"File name change detected: {old_path} has been renamed to {candidate}")
                        matched_current_paths.add(candidate)

                        updated_table[h].remove(old_path)
                        updated_table[h].append(candidate)
                    else:
                        print(f"{old_path}: DELETED")
                        updated_table[h].remove(old_path)

        else:
            for old_path in old_paths:
                print(f"{old_path}: DELETED")
            updated_table.pop(h, None)

    for curr_path, curr_hash in current_path_to_hash.items():
        if curr_path in matched_current_paths:
            continue

        if curr_hash in stored_hash_to_paths:
            print(f"{curr_path}: NEW FILE DETECTED (duplicate content)")
            if curr_hash not in updated_table:
                updated_table[curr_hash] = []
            updated_table[curr_hash].append(curr_path)
        else:
            old_hash = None
            for h, paths in stored_hash_to_paths.items():
                if curr_path in paths:
                    old_hash = h
                    break

            if old_hash:
                print(f"{curr_path}: INVALID (Contents modified)")
                if old_hash in updated_table and curr_path in updated_table[old_hash]:
                    updated_table[old_hash].remove(curr_path)
                    if not updated_table[old_hash]:
                        updated_table.pop(old_hash)

                if curr_hash not in updated_table:
                    updated_table[curr_hash] = []
                updated_table[curr_hash].append(curr_path)
            else:
                print(f"{curr_path}: NEW FILE DETECTED")
                if curr_hash not in updated_table:
                    updated_table[curr_hash] = []
                updated_table[curr_hash].append(curr_path)

    with open(HASH_FILE, "w") as f:
        json.dump(updated_table, f, indent=4)

def main():
    while True:
        print("\n--- Hashing Program ---")
        print("1. Generate New Hash Table")
        print("2. Verify Hashes")
        print("3. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            generate_table()
        elif choice == "2":
            validate_hashes()
        elif choice == "3":
            break
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
