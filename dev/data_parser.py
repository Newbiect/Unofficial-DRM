import struct
import base64

class InitDataParser:
    kKeyIdSize = 16
    kSystemIdSize = 16

    @staticmethod
    def parse(initData, type):
        # Build a list of the key IDs
        keyIds = []
        if type == "kIsoBmffVideoMimeType" or type == "kIsoBmffAudioMimeType" or type == "kCencInitDataFormat":
            res = InitDataParser.parsePssh(initData, keyIds)
            if res != "android::OK":
                return res
        elif type == "kWebmVideoMimeType" or type == "kWebmAudioMimeType" or type == "kWebmInitDataFormat":
            # WebM "init data" is just a single key ID
            if len(initData) != InitDataParser.kKeyIdSize:
                return "android::ERROR_DRM_CANNOT_HANDLE"
            keyIds.append(initData)
        else:
            return "android::ERROR_DRM_CANNOT_HANDLE"
        
        # Build the request
        requestJson = InitDataParser.generateRequest(keyIds)
        licenseRequest = bytearray(requestJson.encode())
        return "android::OK", licenseRequest

    @staticmethod
    def parsePssh(initData, keyIds):
        # Description of PSSH format:
        # https://w3c.github.io/encrypted-media/format-registry/initdata/cenc.html
        readPosition = 0
        expectedSize = len(initData)
        psshIdentifier = b'pssh'
        psshVersion1 = b'\x01\x00\x00\x00'
        keyIdCount = 0
        headerSize = struct.calcsize(">I") + len(psshIdentifier) + len(psshVersion1) + InitDataParser.kSystemIdSize + struct.calcsize(">I")
        if len(initData) < headerSize:
            return "android::ERROR_DRM_CANNOT_HANDLE"
        
        # Validate size field
        expectedSize = struct.unpack(">I", initData[readPosition:readPosition+struct.calcsize(">I")])[0]
        readPosition += struct.calcsize(">I")
        if initData[readPosition:readPosition+4] != struct.pack(">I", expectedSize):
            return "android::ERROR_DRM_CANNOT_HANDLE"
        readPosition += 4
        
        # Validate PSSH box identifier
        if initData[readPosition:readPosition+len(psshIdentifier)] != psshIdentifier:
            return "android::ERROR_DRM_CANNOT_HANDLE"
        readPosition += len(psshIdentifier)
        
        # Validate EME version number
        if initData[readPosition:readPosition+len(psshVersion1)] != psshVersion1:
            return "android::ERROR_DRM_CANNOT_HANDLE"
        readPosition += len(psshVersion1)
        
        # Validate system ID
        if not InitDataParser.isClearKeyUUID(initData[readPosition:readPosition+InitDataParser.kSystemIdSize]):
            return "android::ERROR_DRM_CANNOT_HANDLE"
        readPosition += InitDataParser.kSystemIdSize
        
        # Read key ID count
        keyIdCount = struct.unpack(">I", initData[readPosition:readPosition+struct.calcsize(">I")])[0]
        readPosition += struct.calcsize(">I")
        
        psshSize = 0
        if keyIdCount * InitDataParser.kKeyIdSize != 0:
            psshSize = keyIdCount * InitDataParser.kKeyIdSize
        if readPosition + psshSize != len(initData) - struct.calcsize(">I"):
            return "android::ERROR_DRM_CANNOT_HANDLE"
        
        # Calculate the key ID offsets
        for i in range(keyIdCount):
            keyIdPosition = readPosition + (i * InitDataParser.kKeyIdSize)
            keyIds.append(initData[keyIdPosition:keyIdPosition+InitDataParser.kKeyIdSize])
        
        return "android::OK"

    @staticmethod
    def generateRequest(keyIds):
        kRequestPrefix = "{\"kids\":["
        kRequestSuffix = "],\"type\":\"temporary\"}"
        kBase64Padding = "="
        request = kRequestPrefix
        for i in range(len(keyIds)):
            encodedId = base64.urlsafe_b64encode(keyIds[i]).decode().rstrip("=")
            if i != 0:
                request += ","
            request += "\"" + encodedId + "\""
        request += kRequestSuffix
        # Android's Base64 encoder produces padding. EME forbids padding.
        request = request.replace(kBase64Padding, "")
        return request

# Example usage
initData = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F]
type = "kIsoBmffVideoMimeType"
status, licenseRequest = InitDataParser.parse(initData, type)
print(status)
print(licenseRequest)
