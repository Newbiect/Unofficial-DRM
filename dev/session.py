import logging
from media.stagefright import MediaErrors
from utils import STRING8
from session_lib import SESSION
from aesdecryptor import AESDECRYPTOR
from dataparser import DATAPARSER
from jsonwebkey import JSONWEBKEY

class clearkeydrm:
    def __init__(self):
        self.mMapLock = threading.Lock()
        self.mKeyMap = {}

    def getKeyRequest(self, initData, mimeType):
        parser = InitDataParser()
        return parser.parse(initData, mimeType)

    def provideKeyResponse(self, response):
        responseString = response.decode('utf-8')
        keys = {}
        with self.mMapLock:
            parser = JsonWebKey()
            if parser.extractKeysFromJsonWebKeySet(responseString, keys):
                for keyId, key in keys.items():
                    self.mKeyMap[keyId] = key
                return MediaErrors.OK
            else:
                return MediaErrors.ERROR_DRM_UNKNOWN

    def decrypt(self, keyId, iv, source, subSamples):
        with self.mMapLock:
            keyIdVector = bytearray(keyId)
            if keyIdVector not in self.mKeyMap:
                return MediaErrors.ERROR_DRM_NO_LICENSE
            key = self.mKeyMap[keyIdVector]
            decryptor = AesCtrDecryptor()
            return decryptor.decrypt(key, iv, source, subSamples)
