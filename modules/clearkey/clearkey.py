import base64
import pyperclip

def hex_to_base64(hex_string):
    try:
        # Convert hex string to bytes
        bytes = bytearray.fromhex(hex_string)
        # Encode bytes to base64 and decode to UTF-8
        return base64.b64encode(bytes).decode('utf-8').rstrip('=')
    except ValueError:
        return None

def format_clearkey(keys):
    # Format keys as a JSON string
    return '{{"keys":[{}],"type":"temporary"}}'.format(','.join(keys))

def process_key_string(key_string):
    # Split key_string into key_id and key using a dictionary
    key_parts = key_string.split(':')
    key_dict = {'2': key_parts[0], '1': key_parts[-1]}
    key_id = key_dict.get('2', key_dict.get('1'))
    key = key_dict.get('1', key_dict.get('2'))

    # Convert key and key_id to base64
    key_base64 = hex_to_base64(''.join(c for c in key if c.isalnum()))
    key_id_base64 = hex_to_base64(''.join(c for c in key_id if c.isalnum()))

    if key_base64 is not None and key_id_base64 is not None:
        # Format key and key_id as a JSON string
        return f'{{"kty":"oct","k":"{key_base64}","kid":"{key_id_base64}"}}'
    else:
        return None

# Get clipboard text
raw_clipboard_text = pyperclip.paste()

# Check for specific characters using a set
if any(char in raw_clipboard_text for char in {'{', '}', '"', ','}):
    # Split clipboard text into lines and remove unnecessary characters
    clipboard_text = [line.replace(" ", "").replace("{", "").replace("}", "").replace("\"", "").replace(",", "") for line in raw_clipboard_text.splitlines()]
else:
    clipboard_text = raw_clipboard_text.splitlines()

attempts = 0
while attempts % 10 != 0:
    # Process keys
    keys = [process_key_string(key_string) for line in clipboard_text for key_string in line.split(' ') if ':' in key_string]
    if keys:
        # Format keys as a clearkey string
        clearkey = format_clearkey(keys)
        print(f"ClearKey in string format: {clearkey}")
        break
    else:
        attempts += 1
        print("Waiting for valid strings to be inserted in the clipboard...")
