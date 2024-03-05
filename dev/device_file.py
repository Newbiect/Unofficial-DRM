import hashlib
import os
import shutil

LICENSE_FILE_EXT = ".lic"


def hash_data(data):
    hash_object = hashlib.sha256(data.encode())
    return hash_object.hexdigest()


def store_license(key_set_id, state, license_response):
    file = {
        "type": "LICENSE",
        "version": "VERSION_1",
        "license": {
            "state": state,
            "license": license_response
        }
    }
    serialized_file = str(file)
    file_name = key_set_id + LICENSE_FILE_EXT
    return store_file_with_hash(file_name, serialized_file)


def store_file_with_hash(file_name, serialized_file):
    hash_value = hash_data(serialized_file)
    hash_file = {
        "file": serialized_file,
        "hash": hash_value
    }
    serialized_hash_file = str(hash_file)
    return store_file_raw(file_name, serialized_hash_file)


def store_file_raw(file_name, serialized_hash_file):
    file_size = len(serialized_hash_file)
    with open(file_name, "w") as f:
        f.write(serialized_hash_file)
    if os.path.getsize(file_name) != file_size:
        print(f"StoreFileRaw: Failed to write {file_name}")
        return False
    print(f"StoreFileRaw: wrote {file_size} bytes to {file_name}")
    return True


def retrieve_license(key_set_id):
    file_name = key_set_id + LICENSE_FILE_EXT
    file_data = retrieve_hashed_file(file_name)
    if not file_data:
        return False
    if file_data["type"] != "LICENSE":
        print("RetrieveLicense: Invalid file type")
        return False
    if file_data["version"] != "VERSION_1":
        print("RetrieveLicense: Invalid file version")
        return False
    if "license" not in file_data:
        print("RetrieveLicense: License not present")
        return False
    license_data = file_data["license"]
    state = license_data["state"]
    offline_license = license_data["license"]
    return state, offline_license


def delete_license(key_set_id):
    file_name = key_set_id + LICENSE_FILE_EXT
    if os.path.exists(file_name):
        os.remove(file_name)
        return True
    return False


def delete_all_licenses():
    for file_name in os.listdir():
        if file_name.endswith(LICENSE_FILE_EXT):
            os.remove(file_name)
    return True


def license_exists(key_set_id):
    file_name = key_set_id + LICENSE_FILE_EXT
    return os.path.exists(file_name)


def list_licenses():
    licenses = []
    for file_name in os.listdir():
        if file_name.endswith(LICENSE_FILE_EXT):
            licenses.append(file_name[:-len(LICENSE_FILE_EXT)])
    return licenses


def retrieve_hashed_file(file_name):
    if not os.path.exists(file_name):
        print(f"RetrieveHashedFile: {file_name} does not exist")
        return None
    file_size = os.path.getsize(file_name)
    with open(file_name, "r") as f:
        serialized_hash_file = f.read()
    if len(serialized_hash_file) != file_size:
        print(f"RetrieveHashedFile: Failed to read from {file_name}")
        return None
    hash_file = eval(serialized_hash_file)
    hash_value = hash_data(hash_file["file"])
    if hash_value != hash_file["hash"]:
        print("RetrieveHashedFile: Hash mismatch")
        return None
    return eval(hash_file["file"])


def remove_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
        return True
    return False


def get_file_size(file_name):
    if os.path.exists(file_name):
        return os.path.getsize(file_name)
    return -1