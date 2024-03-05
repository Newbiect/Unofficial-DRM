import base64
import struct

class InitDataParser:
    kKeyIdSize = 16
    kSystemIdSize = 16

    @staticmethod
    def parse(init_data, mime_type, key_type):
        key_ids = []
        if mime_type == "video/mp4" or mime_type == "audio/mp4" or mime_type == "cenc":
            res = InitDataParser.parse_pssh(init_data, key_ids)
            if res != "OK":
                return res
        elif mime_type == "video/webm" or mime_type == "audio/webm" or mime_type == "webm":
            if len(init_data) != InitDataParser.kKeyIdSize:
                return "ERROR_CANNOT_HANDLE"
            key_ids.append(init_data)
        else:
            return "ERROR_CANNOT_HANDLE"

        if key_type == "release":
            # restore key
            pass

        request_json = InitDataParser.generate_request(key_type, key_ids)
        license_request = request_json.encode("utf-8")
        return "OK", license_request

    @staticmethod
    def parse_pssh(init_data, key_ids):
        expected_size = len(init_data)
        pssh_identifier = b"pssh"
        pssh_version1 = struct.pack(">I", 1)
        key_id_count = 0
        header_size = (
            struct.calcsize(">I")
            + len(pssh_identifier)
            + len(pssh_version1)
            + InitDataParser.kSystemIdSize
            + struct.calcsize(">I")
        )
        if len(init_data) < header_size:
            return "ERROR_CANNOT_HANDLE"

        # Validate size field
        if struct.unpack(">I", init_data[:4])[0] != expected_size:
            return "ERROR_CANNOT_HANDLE"

        read_position = struct.calcsize(">I")
        # Validate PSSH box identifier
        if init_data[read_position : read_position + len(pssh_identifier)] != pssh_identifier:
            return "ERROR_CANNOT_HANDLE"

        read_position += len(pssh_identifier)
        # Validate EME version number
        if init_data[read_position : read_position + len(pssh_version1)] != pssh_version1:
            return "ERROR_CANNOT_HANDLE"

        read_position += len(pssh_version1)
        # Validate system ID
        if not InitDataParser.is_clear_key_uuid(init_data[read_position : read_position + InitDataParser.kSystemIdSize]):
            return "ERROR_CANNOT_HANDLE"

        read_position += InitDataParser.kSystemIdSize
        # Read key ID count
        key_id_count = struct.unpack(">I", init_data[read_position : read_position + struct.calcsize(">I")])[0]
        read_position += struct.calcsize(">I")

        pssh_size = key_id_count * InitDataParser.kKeyIdSize
        if pssh_size != expected_size - struct.calcsize(">I"):
            return "ERROR_CANNOT_HANDLE"

        # Calculate the key ID offsets
        for i in range(key_id_count):
            key_id_position = read_position + (i * InitDataParser.kKeyIdSize)
            key_ids.append(init_data[key_id_position : key_id_position + InitDataParser.kKeyIdSize])

        return "OK"

    @staticmethod
    def is_clear_key_uuid(system_id):
        clear_key_uuid = b"\xE2\x9A\xA0\xEF\xA3\xA6\xEF\xA3\xA7\xEF\xA3\xA8\xEF\xA3\xA9\xEF\xA3\xAA\xEF\xA3\xAB"
        return system_id == clear_key_uuid

    @staticmethod
    def generate_request(key_type, key_ids):
        request_prefix = "{\"kids\":["
        temporary_session = "],\"type\":\"temporary\"}"
        persistent_session = "],\"type\":\"persistent-license\"}"
        request = request_prefix
        for i, key_id in enumerate(key_ids):
            encoded_id = base64.urlsafe_b64encode(key_id).decode("utf-8")
            if i != 0:
                request += ","
            request += "\"" + encoded_id + "\""

        if key_type == "streaming":
            request += temporary_session
        elif key_type == "offline" or key_type == "release":
            request += persistent_session

        # Android's Base64 encoder produces padding. EME forbids padding.
        request = request.replace("=", "")
        return request