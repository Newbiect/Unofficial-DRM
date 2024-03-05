import logging
from typing import List, Dict
from threading import Lock
from init_data_parser import InitDataParser
from Crypto.Cipher import AES

logger = logging.getLogger("clearkey-Session")

class Session:
    def __init__(self):
        self.key_map: Dict[List[int], List[int]] = {}
        self.map_lock = Lock()

    def get_key_request(self, init_data: List[int], mime_type: str, key_type: int) -> int:
        # Parse the init data
        parser = InitDataParser()
        key_request = []
        response_type = parser.parse(init_data, mime_type, key_type, key_request)
        return response_type

    def provide_key_response(self, response: List[int]) -> int:
        response_string = bytes(response).decode()
        keys = {}
        with self.map_lock:
            parser = JsonWebKey()
            if parser.extract_keys_from_json_web_key_set(response_string, keys):
                for key, value in keys.items():
                    key_bytes = list(key)
                    value_bytes = list(value)
                    self.key_map[key_bytes] = value_bytes
                return 0
            else:
                return -1

    def decrypt(self, key_id: List[int], iv: List[int], src_ptr: bytes, dest_ptr: bytearray,
                clear_data_lengths: List[int], encrypted_data_lengths: List[int]) -> int:
        with self.map_lock:
            if self.get_mock_error() != 0:
                return self.get_mock_error()

            key_id_bytes = list(key_id)
            if key_id_bytes not in self.key_map:
                return -2

            key = bytes(self.key_map[key_id_bytes])
            decryptor = AES.new(key, AES.MODE_CTR, nonce=bytes(iv))
            decrypted_data = decryptor.decrypt(src_ptr)
            dest_ptr[:len(decrypted_data)] = decrypted_data

            return 0