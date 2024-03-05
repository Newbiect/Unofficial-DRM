import jwt
import requests

license_server_url = "https://widevine-license.appspot.com/getlicense"
key_set_id = "5ca70c8e-2a7d-4a4c-a0b5-8c9a870cf6af"
content_id = "YOUR_CONTENT_ID"
policy_sei_message = "YOUR_POLICY_SEI_MESSAGE"
video_id = "YOUR_VIDEO_ID"
output_protection = "2"
device_id = "YOUR_DEVICE_ID"
pssh = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x80"
system_id = "4a454c4c-4f4e-5445-4544-4943414d4544"
provider_id = "c4c1996e-7ecf-4646-a4a4-4c414e444544"
cryptogram_type = "0"
license_duration = 3600
license_server_cert = "YOUR_LICENSE_SERVER_CERTIFICATE"
private_key = "YOUR_PRIVATE_KEY"

header = {"alg": "RS256","typ": "JWT"}
payload = {
    "format": "common_centered",
    "widevine_message": {
        "key_set_id": key_set_id,
        "content_id": content_id,
        "policy_sei_message": policy_sei_message,
        "video_id": video_id,
        "output_protection": output_protection,
        "pssh": psssh,
        "system_id": system_id,
        "provider_id": provider_id,
        "cryptogram_type": cryptogram_type,
        "device_id": device_id,
        "license_duration": license_duration
    }
}
jwt_token = jwt.encode(payload, private_key, algorithm="RS256", headers=header)
headers = {"X-Goog-Api-Key": "YOUR_API_KEY","X-Goog-User-Agent": "YOUR_USER_AGENT","X-Goog-License-Server-Key": key_set_id,"Content-Type": "application/json","Accept": "application/json"}

# Set the license server request data
data = {
    "pssh": psssh,
    "provider": provider_id.lower(),
    "license_server_cert": license_server_cert,
    "signed_request": jwt_token
}
session = requests.Session()
response = session.post(license_server_url, headers=headers, json=data, verify=False)

if response.status_code == 200:
    # Extract the license from the response
    license = response.content

    with open("license.bin", "wb") as f:
        f.write(license)
else:
    raise Exception("Failed to obtain license from Widevine license server.")
