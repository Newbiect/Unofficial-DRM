import logging
from typing import List
from uuid import UUID
from drm_plugin import SessionLibrary, Session

class DrmFactory:
    def __init__(self):
        self.supported_uuids = [UUID('1077efec-c0b2-4d02-ace3-3c1e52e2fb4b')]
        self.supported_content_types = [
            'video/mp4',
            'audio/mp4',
            'application/octet-stream',
            'video/webm',
            'audio/webm',
            'application/webm'
        ]
    
    def is_crypto_scheme_supported(self, uuid: UUID) -> bool:
        return uuid in self.supported_uuids
    
    def is_content_type_supported(self, content_type: str) -> bool:
        return content_type in self.supported_content_types
    
    def create_drm_plugin(self, uuid: UUID) -> 'DrmPlugin':
        if not self.is_crypto_scheme_supported(uuid):
            return None
        return DrmPlugin(SessionLibrary.get())

class DrmPlugin:
    def __init__(self, session_library):
        self.session_library = session_library

# Usage example
factory = DrmFactory()
uuid = UUID('1077efec-c0b2-4d02-ace3-3c1e52e2fb4b')
plugin = factory.create_drm_plugin(uuid)
if plugin is not None:
    logging.info("DrmPlugin created successfully")
else:
    logging.error("Unsupported crypto scheme")
