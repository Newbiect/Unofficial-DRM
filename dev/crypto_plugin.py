import logging
from media.stagefright.MediaErrors import ERROR_DRM_CANNOT_HANDLE, ERROR_DRM_DECRYPT, ERROR_DRM_SESSION_NOT_OPENED
from crypto_plugin import CryptoPlugin
from dev.session_library import SessionLibrary

class ClearKeyCryptoPlugin(CryptoPlugin):
    def __init__(self):
        self.mSession = None

    def decrypt(self, secure, keyId, iv, mode, pattern, srcPtr, subSamples, numSubSamples, dstPtr, errorDetailMsg):
        if secure:
            errorDetailMsg.setTo("Secure decryption is not supported with ClearKey.")
            return ERROR_DRM_CANNOT_HANDLE

        if mode == CryptoPlugin.kMode_Unencrypted:
            offset = 0
            for i in range(numSubSamples):
                subSample = subSamples[i]
                if subSample.mNumBytesOfEncryptedData != 0:
                    errorDetailMsg.setTo("Encrypted subsamples found in allegedly unencrypted data.")
                    return ERROR_DRM_DECRYPT
                if subSample.mNumBytesOfClearData != 0:
                    dstPtr[offset:offset+subSample.mNumBytesOfClearData] = srcPtr[offset:offset+subSample.mNumBytesOfClearData]
                    offset += subSample.mNumBytesOfClearData
            return offset

        elif mode == CryptoPlugin.kMode_AES_CTR:
            bytesDecrypted = 0
            res = self.mSession.decrypt(keyId, iv, srcPtr, dstPtr, subSamples, numSubSamples, bytesDecrypted)
            if res == CryptoPlugin.OK:
                return bytesDecrypted
            else:
                errorDetailMsg.setTo("Decryption Error")
                return res

        else:
            errorDetailMsg.setTo("Selected encryption mode is not supported by the ClearKey DRM Plugin.")
            return ERROR_DRM_CANNOT_HANDLE

    def setMediaDrmSession(self, sessionId):
        if not sessionId:
            self.mSession = None
        else:
            self.mSession = SessionLibrary.get().findSession(sessionId)
            if not self.mSession:
                return ERROR_DRM_SESSION_NOT_OPENED
        return CryptoPlugin.OK