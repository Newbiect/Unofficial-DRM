import logging
from typing import List, Dict

# Define the logger
logger = logging.getLogger(__name__)

# Define the MockDrmCryptoPlugin class
class MockDrmCryptoPlugin:
    def __init__(self):
        self.mock_uuid = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f, 0x10]
        self.mock_initdata = []
        self.mock_mimetype = ""
        self.mock_keytype = ""
        self.mock_optparams = {}
        self.mock_request = []
        self.mock_defaultUrl = ""
        self.mock_keyRequestType = ""
        self.mock_response = []
        self.mock_secure_stop = []
        self.mock_secure_stop1 = []
        self.mock_secure_stop2 = []
        self.mock_ssrelease = []
        self.mock_sessions = []
        self.mock_keySets = []
        self.mock_stringProperties = {}
        self.mock_byteArrayProperties = {}

    def isCryptoSchemeSupported(self, uuid: List[int]) -> bool:
        return uuid == self.mock_uuid

    def isContentTypeSupported(self, mimeType: str) -> bool:
        if mimeType != "video/mp4":
            return False
        return True

    def createDrmPlugin(self, uuid: List[int]) -> None:
        return MockDrmPlugin()

    def createCryptoPlugin(self, uuid: List[int]) -> None:
        return MockCryptoPlugin()

    def getPropertyString(self, name: str) -> str:
        if name in self.mock_stringProperties:
            return self.mock_stringProperties[name]
        else:
            logger.error(f"No property found for name: {name}")
            return ""

    def getPropertyByteArray(self, name: str) -> List[int]:
        if name in self.mock_byteArrayProperties:
            return self.mock_byteArrayProperties[name]
        else:
            logger.error(f"No property found for name: {name}")
            return []

    def setPropertyString(self, name: str, value: str) -> None:
        self.mock_stringProperties[name] = value

    def setPropertyByteArray(self, name: str, value: List[int]) -> None:
        self.mock_byteArrayProperties[name] = value

    def setCipherAlgorithm(self, sessionId: List[int], algorithm: str) -> None:
        logger.info(f"Setting cipher algorithm for sessionId: {sessionId} to {algorithm}")
        return

    def setMacAlgorithm(self, sessionId: List[int], algorithm: str) -> None:
        logger.info(f"Setting MAC algorithm for sessionId: {sessionId} to {algorithm}")
        return

    def encrypt(self, sessionId: List[int], keyId: List[int], input: List[int], iv: List[int]) -> List[int]:
        logger.info(f"Encrypting data for sessionId: {sessionId}, keyId: {keyId}, input: {input}, iv: {iv}")
        return []

    def decrypt(self, sessionId: List[int], keyId: List[int], input: List[int], iv: List[int]) -> List[int]:
        logger.info(f"Decrypting data for sessionId: {sessionId}, keyId: {keyId}, input: {input}, iv: {iv}")
        return []

    def sign(self, sessionId: List[int], keyId: List[int], message: List[int]) -> List[int]:
        logger.info(f"Signing message for sessionId: {sessionId}, keyId: {keyId}, message: {message}")
        return []

    def verify(self, sessionId: List[int], keyId: List[int], message: List[int], signature: List[int]) -> bool:
        logger.info(f"Verifying signature for sessionId: {sessionId}, keyId: {keyId}, message: {message}, signature: {signature}")
        return False

# Define the MockDrmPlugin class
class MockDrmPlugin:
    def __init__(self):
        self.mock_sessions = []

    def openSession(self) -> List[int]:
        sessionId = []
        self.mock_sessions.append(sessionId)
        logger.info(f"Opening session with sessionId: {sessionId}")
        return sessionId

    def closeSession(self, sessionId: List[int]) -> None:
        if sessionId in self.mock_sessions:
            self.mock_sessions.remove(sessionId)
            logger.info(f"Closing session with sessionId: {sessionId}")
        else:
            logger.error(f"Invalid sessionId: {sessionId}")

    def getKeyRequest(self, sessionId: List[int], initData: List[int], mimeType: str, keyType: str, optionalParameters: Dict[str, str]) -> List[int]:
        logger.info(f"Getting key request for sessionId: {sessionId}, initData: {initData}, mimeType: {mimeType}, keyType: {keyType}, optionalParameters: {optionalParameters}")
        return []

    def provideKeyResponse(self, sessionId: List[int], response: List[int]) -> List[int]:
        logger.info(f"Providing key response for sessionId: {sessionId}, response: {response}")
        return []

    def removeKeys(self, keySetId: List[int]) -> None:
        logger.info(f"Removing keys for keySetId: {keySetId}")
        return

    def restoreKeys(self, sessionId: List[int], keySetId: List[int]) -> None:
        logger.info(f"Restoring keys for sessionId: {sessionId}, keySetId: {keySetId}")
        return

    def queryKeyStatus(self, sessionId: List[int]) -> Dict[str, str]:
        logger.info(f"Querying key status for sessionId: {sessionId}")
        return {}

    def getProvisionRequest(self, certType: str, certAuthority: str) -> List[int]:
        logger.info(f"Getting provision request for certType: {certType}, certAuthority: {certAuthority}")
        return []

    def provideProvisionResponse(self, response: List[int]) -> None:
        logger.info(f"Providing provision response for response: {response}")
        return

    def getSecureStop(self, ssid: List[int]) -> List[int]:
        logger.info(f"Getting secure stop for ssid: {ssid}")
        return []

    def getSecureStops(self) -> List[List[int]]:
        logger.info("Getting secure stops")
        return []

    def releaseSecureStops(self, ssRelease: List[int]) -> None:
        logger.info(f"Releasing secure stops for ssRelease: {ssRelease}")
        return

    def releaseAllSecureStops(self) -> None:
        logger.info("Releasing all secure stops")
        return

# Define the MockCryptoPlugin class
class MockCryptoPlugin:
    def __init__(self):
        pass

    def requiresSecureDecoderComponent(self, mime: str) -> bool:
        logger.info(f"Checking if secure decoder component is required for mime: {mime}")
        return False

    def decrypt(self, secure: bool, key: List[int], iv: List[int], mode: str, pattern: Dict[str, int], srcPtr: int, subSamples: List[Dict[str, int]], numSubSamples: int, dstPtr: int) -> int:
        logger.info(f"Decrypting data with secure: {secure}, key: {key}, iv: {iv}, mode: {mode}, pattern: {pattern}, srcPtr: {srcPtr}, subSamples: {subSamples}, numSubSamples: {numSubSamples}, dstPtr: {dstPtr}")
        return 0

# Shared library entry point
def createDrmFactory() -> MockDrmCryptoPlugin:
    return MockDrmCryptoPlugin()

# Shared library entry point
def createCryptoFactory() -> MockDrmCryptoPlugin:
    return MockDrmCryptoPlugin()
