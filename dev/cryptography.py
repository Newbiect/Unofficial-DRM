import logging
from typing import List
from crypto_plugin import ClearKeyCryptoPlugin

class CryptoFactory:
    def __init__(self):
        self.logger = logging.getLogger("ClearKeyCryptoFactory")

    def isCryptoSchemeSupported(self, uuid: List[int]) -> bool:
        return self.isClearKeyUUID(uuid)

    def createPlugin(self, uuid: List[int], data: bytes, size: int) -> ClearKeyCryptoPlugin:
        if not self.isCryptoSchemeSupported(uuid):
            return None, "BAD_VALUE"

        sessionId = list(data)
        clearKeyPlugin = ClearKeyCryptoPlugin(sessionId)
        result = clearKeyPlugin.getInitStatus()
        if result == "OK":
            return clearKeyPlugin, result
        else:
            return None, result