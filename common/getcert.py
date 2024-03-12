import requests
import base64

# Define the URLs and data
challenge_api_url = "https://early-numbers-film-172-104-181-21.loca.lt/pywidevine"
keys_api_url = "https://early-numbers-film-172-104-181-21.loca.lt/keys"
license_url = "https://cwip-shaka-proxy.appspot.com/no_auth"

api_headers = {"Bypass-Tunnel-Reminder": "Yes"}

pssh = "AAAAW3Bzc2gAAAAA7e+LqXnWSs6jyCfc1R0h7QAAADsIARIQ62dqu8s0Xpa7z2FmMPGj2hoNd2lkZXZpbmVfdGVzdCIQZmtqM2xqYVNkZmFsa3IzaioCSEQyAA=="

license_headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept': '*/*',
    'origin': 'https://bitmovin.com',
    'referer': 'https://bitmovin.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-type': 'application/x-www-form-urlencoded',
    'x-forwarded-for': '127.0.0.1'
}

challenge_api_data = {"pssh": None, "certificate": None}
keys_api_data = {"session_id": None, "license": None}

try:
    challenge_api_data["pssh"] = pssh
    challenge_api_request = requests.post(challenge_api_url, json=challenge_api_data, headers=api_headers)
    challenge_api_request.raise_for_status()  # Raise an error for HTTP errors
    challenge_api_request_json = challenge_api_request.json()

    challenge_b64 = challenge_api_request_json.get("challenge")
    session_id = challenge_api_request_json.get("session_id")

    challenge_raw = base64.b64decode(challenge_b64)

    license_raw = requests.post(license_url, headers=license_headers, data=challenge_raw)
    license_raw.raise_for_status()

    license_b64 = base64.b64encode(license_raw.content).decode()

    keys_api_data["session_id"] = session_id
    keys_api_data["license"] = license_b64

    keys_api_request = requests.post(keys_api_url, json=keys_api_data, headers=api_headers)
    keys_api_request.raise_for_status()  # Raise an error for HTTP errors
    keys = keys_api_request.json().get("keys")  # Extract the keys
    
    print(keys)

except requests.exceptions.RequestException as e:
    print("An error occurred during the request:", e)

except KeyError as e:
    print("A required key is missing in the response:", e)