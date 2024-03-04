import base64
import datetime
import json
import time
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA

license_payload = {
    "provider": "widevine",
    "content_id": "your_content_id",
    "policy_id": "your_policy_id",
    "roots": {
        "widevine": [
            "your_widevine_root_certificate"
        ]
    },
    "roles": {
        "com.widevine.alpha": {
            "origin": "com.widevine.alpha",
            "url": "widevine-license-url"
        }
    },
    "date_time": int(time.time())
}

key_system = {
    "widevine": {
        "server_url": "your_license_server_url",
        "hdcp_policy": "hdcp_policy",
        "license_duration_seconds": 31536000,
        "playback_system_properties": {
            "android_device_properties": {
                "device_brand": "your_device_brand",
                "device_model": "your_device_model",
                "os_version": "your_os_version",
                "manufacturer": "your_manufacturer"
            }
        }
    }
}

key_system_parameters = {
    "com.widevine.alpha": {
        "method": "aes-128-ctr",
        "key_format": "raw",
        "key_length": 16,
        "iv_format": "raw",
        "iv_length": 16
    }
}

key = get_random_bytes(16)
iv = get_random_bytes(16)

cipher = AES.new(key, AES.MODE_CTR, nonce=iv)
encrypted_license_payload = cipher.encrypt(json.dumps(license_payload).encode())
rsa_key = RSA.generate(2048)

license_challenge = {
    "pssh_box": {
        "kid": base64.b64encode(rsa_key.publickey().export_key()).decode(),
        "iv": iv.hex(),
        "data": encrypted_license_payload.hex()
    }
}

signature = pkcs1_15.new(rsa_key).sign(SHA256.new(json.dumps(license_challenge).encode()))
license_response = {
    "keys": [{
        "kty": "RSA",
        "n": rsa_key.export_key().hex(),
        "alg": "RS256",
        "use": "sig",
        "kid": base64.b64encode(rsa_key.publickey().export_key()).decode()
    }],
    "key_systems": [key_system],
    "messages": [{
        "type": "com.widevine.alpha",
        "value": base64.b64encode(encrypted_license_payload).decode(),
        "iv": iv.hex(),
        "signatures": [{
            "kid": base64.b64encode(rsa_key.publickey().export_key()).decode(),
            "header": base64.b64encode(json.dumps(license_challenge).encode()).decode(),
            "signature": base64.b64encode(signature).decode()
        }]
    }],
    "date_time": int(time.time())
}

print(license_response)
