import requests
import base64
import time
import json
import coloredlogs
import logging
from colorama import Fore

coloredlogs.install(level='DEBUG')

started = time.time()
api_base_url = "https://kepala-pantas.xyz/dev/chromeOS/"
api_cdm_device = "CHROME"
api_headers = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJZV1J0YVc0PSIsImp0aSI6Ijk5ZTU4ZWFmLTIzODgtNGUzZC05ZGNlLTY1YWViNTA1OGE0ZCIsInVzZXJuYW1lIjoiYWRtaW4iLCJ1c2VyX2lkIjoiMzc5ODZlNDE3NDQ0NDk1MThjNzZjMWRiMmQyMjI2YmYifQ.rR-CJyNpQ87R4qrFxmhXvMAEzZMg6lFDD66aR_eJEFyHk8jWnIgBAwdoywK2sSfBQq3wZENVtIdfNkqX-YW6LbJQqud6VCchNrWtKKGcEPt-pKENkVuS-W3afFyOdL0572_CMhyLcir56C-2gmbFcNh7qCQuECS95wV6yWxiG2YT3OJ77xzLz6NxRw6thGVi9Wt6bDBDSg8USTgxSl5Q4fyAj7w0EEnm4ZPlRQnLUTawcun5W1gDatkI_u0BpwPofARUOJXiKlJBR1ZBEkm7kLw51G3SEzp35RsdeCYi8vhRcQx6v34Ah5PA8GABDcYb_JDYKY8ozYbEBbFyJn4T5w',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept': '*/*',
}
session = requests.Session()
session.headers.update(api_headers)

# Logging
logging.info("Requesting to open session...")
open_session = session.get(api_base_url + api_cdm_device + '/open').json()
session_id = open_session["responseData"]["sessionId"]
challenge_api_data = {'session_id': session_id , 'init_data': None}

pssh = input(Fore.YELLOW + "PSSH: " + Fore.WHITE)
license_url = input(Fore.YELLOW + "License URL: " + Fore.WHITE)
license_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36','accept': '*/*'}

logging.info("Requesting service certificate...")
service_certificate = requests.post(license_url, headers=license_headers, data=base64.b64decode("CAQ=")).content
service_certificate_b64 = base64.b64encode(service_certificate).decode()
set_certificate = session.post(api_base_url + api_cdm_device + '/set_service_certificate', json={'session_id': session_id , 'certificate': service_certificate_b64}, headers=api_headers).json()

logging.info("Requesting license challenge...")
challenge_api_data["init_data"] = pssh
challenge_api_request = session.post(api_base_url + api_cdm_device + '/get_license_challenge/STREAMING', json=challenge_api_data).json() # License request challenge is returned in base64.

challenge_b64 = challenge_api_request['data']["challenge_b64"]
challenge_raw = base64.b64decode(challenge_b64)

license_raw = requests.post(license_url, headers=license_headers, data=challenge_raw).content
license_b64 = base64.b64encode(license_raw).decode()

parse_license_data = {'session_id': session_id , 'license_message': license_b64}
license_api_request = requests.post(api_base_url + api_cdm_device + '/parse_license', json=parse_license_data, headers=api_headers).json()

logging.info("Requesting keys...")
keys_api_data = {'session_id': session_id}
keys_api_request = requests.post(api_base_url + api_cdm_device + '/get_keys/CONTENT', json=keys_api_data, headers=api_headers).json()
keys = keys_api_request['data']['keys']

formatted_keys = []
for key in keys:
    key_id = key['key_id']
    key_value = key['key']
    formatted_keys.append({"kid": key_id, "key": key_value})

open_session['responseData']['keys'] = formatted_keys

logging.info("Printing open session JSON...")
print(Fore.YELLOW, json.dumps(open_session, indent=4))

logging.info("Closing session...")
close_session = session.get(api_base_url + api_cdm_device + '/close/' + session_id, headers=api_headers).text

finished = time.time()
complete_time = int(finished - started)
logging.info(f"Time Taken : {complete_time}s")
