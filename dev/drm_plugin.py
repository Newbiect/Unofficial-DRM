import logging
from media.stagefright import MediaErrors
from utils import StrongPointer
from drm_plugin import DrmPlugin
from drm_plugin import ClearKeyDrmProperties
from clearkey import clearkeydrm

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DrmPlugin(DrmPlugin):
    def __init__(self, sessionLibrary):
        super().__init__(sessionLibrary)
        self.mPlayPolicy = {}
        self.initProperties()

    def initProperties(self):
        self.mStringProperties = {}
        self.mStringProperties['kVendorKey'] = 'kVendorValue'
        self.mStringProperties['kVersionKey'] = 'kVersionValue'
        self.mStringProperties['kPluginDescriptionKey'] = 'kPluginDescriptionValue'
        self.mStringProperties['kAlgorithmsKey'] = 'kAlgorithmsValue'
        self.mStringProperties['kListenerTestSupportKey'] = 'kListenerTestSupportValue'
        testDeviceId = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
        self.mByteArrayProperties = {'kDeviceIdKey': testDeviceId}

    def openSession(self, sessionId):
        session = self.mSessionLibrary.createSession()
        sessionId = session.sessionId()
        return MediaErrors.OK

    def closeSession(self, sessionId):
        session = self.mSessionLibrary.findSession(sessionId)
        if len(sessionId) == 0:
            return MediaErrors.BAD_VALUE
        if session:
            self.mSessionLibrary.destroySession(session)
            return MediaErrors.OK
        return MediaErrors.ERROR_DRM_SESSION_NOT_OPENED

    def getKeyRequest(self, scope, initData, mimeType, keyType, optionalParameters, request, defaultUrl, keyRequestType):
        if len(scope) == 0:
            return MediaErrors.BAD_VALUE
        if keyType != DrmPlugin.kKeyType_Streaming:
            return MediaErrors.ERROR_DRM_CANNOT_HANDLE
        keyRequestType = DrmPlugin.kKeyRequestType_Initial
        defaultUrl = ''
        session = self.mSessionLibrary.findSession(scope)
        if not session:
            return MediaErrors.ERROR_DRM_SESSION_NOT_OPENED
        return session.getKeyRequest(initData, mimeType, request)

    def setPlayPolicy(self):
        self.mPlayPolicy = {}
        self.mPlayPolicy['kQueryKeyLicenseType'] = 'kStreaming'
        self.mPlayPolicy['kQueryKeyPlayAllowed'] = 'kTrue'
        self.mPlayPolicy['kQueryKeyRenewAllowed'] = 'kTrue'

    def provideKeyResponse(self, scope, response, keySetId):
        if len(scope) == 0 or len(response) == 0:
            return MediaErrors.BAD_VALUE
        session = self.mSessionLibrary.findSession(scope)
        if not session:
            return MediaErrors.ERROR_DRM_SESSION_NOT_OPENED
        self.setPlayPolicy()
        res = session.provideKeyResponse(response)
        if res == MediaErrors.OK:
            keySetId = []
        return res

    def getPropertyByteArray(self, name, value):
        if name not in self.mByteArrayProperties:
            logger.error("App requested unknown property: %s", name)
            return MediaErrors.ERROR_DRM_CANNOT_HANDLE
        value = self.mByteArrayProperties[name]
        return MediaErrors.OK

    def setPropertyByteArray(self, name, value):
        if name == 'kDeviceIdKey':
            logger.debug("Cannot set immutable property: %s", name)
            return MediaErrors.ERROR_DRM_CANNOT_HANDLE
        logger.error("Failed to set property byte array, key=%s", name)
        return MediaErrors.ERROR_DRM_CANNOT_HANDLE

    def getPropertyString(self, name, value):
        if name not in self.mStringProperties:
            logger.error("App requested unknown property: %s", name)
            return MediaErrors.ERROR_DRM_CANNOT_HANDLE
        value = self.mStringProperties[name]
        return MediaErrors.OK

    def setPropertyString(self, name, value):
        immutableKeys = [kAlgorithmsKey, kPluginDescriptionKey, kVendorKey, kVersionKey]
        if name in immutableKeys:
            logger.debug("Cannot set immutable property: %s", name)
            return MediaErrors.ERROR_DRM_CANNOT_HANDLE
        if name not in self.mStringProperties:
            logger.error("Cannot set undefined property string, key=%s", name)
            return MediaErrors.ERROR_DRM_CANNOT_HANDLE
        self.mStringProperties[name] = value
        return MediaErrors.OK

    def queryKeyStatus(self, sessionId, infoMap):
        if len(sessionId) == 0:
            return MediaErrors.BAD_VALUE
        infoMap = self.mPlayPolicy
        return MediaErrors.OK

sessionLibrary = SessionLibrary()
drmPlugin = DrmPlugin(sessionLibrary)