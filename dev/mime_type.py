import logging

class MimeTypeUtil:
    mime_type_audio_mpeg = "audio/mpeg"
    mime_type_audio_3gpp = "audio/3gpp"
    mime_type_audio_amr = "audio/amr-wb"
    mime_type_audio_aac = "audio/mp4a-latm"
    mime_type_audio_wav = "audio/wav"
    mime_type_video_mpeg4 = "video/mpeg4"
    mime_type_video_3gpp = "video/3gpp"
    
    mime_group_audio = "audio/"
    mime_group_application = "application/"
    mime_group_image = "image/"
    mime_group_video = "video/"
    mime_type_unsupported = "unsupported/drm.mimetype"
    
    mimeGroup = [
        {"type": 0, "pGroup": mime_group_audio, "size": len(mime_group_audio)},
        {"type": 1, "pGroup": mime_group_application, "size": len(mime_group_application)},
        {"type": 2, "pGroup": mime_group_image, "size": len(mime_group_image)},
        {"type": 3, "pGroup": mime_group_video, "size": len(mime_group_video)},
        {"type": -1, "pGroup": None, "size": 0}
    ]
    
    mimeTypeList = [
        {"type": 0, "pMimeExt": "mp3", "size": len("mp3"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "x-mpeg", "size": len("x-mpeg"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "x-mp3", "size": len("x-mp3"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "mpg", "size": len("mpg"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "mpg3", "size": len("mpg3"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "x-mpg", "size": len("x-mpg"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "x-mpegaudio", "size": len("x-mpegaudio"), "pMimeType": mime_type_audio_mpeg},
        {"type": 0, "pMimeExt": "3gp", "size": len("3gp"), "pMimeType": mime_type_audio_3gpp},
        {"type": 0, "pMimeExt": "amr", "size": len("amr"), "pMimeType": mime_type_audio_amr},
        {"type": 0, "pMimeExt": "aac", "size": len("aac"), "pMimeType": mime_type_audio_aac},
        {"type": 0, "pMimeExt": "x-wav", "size": len("x-wav"), "pMimeType": mime_type_audio_wav},
        {"type": 3, "pMimeExt": "mpg4", "size": len("mpg4"), "pMimeType": mime_type_video_mpeg4},
        {"type": 3, "pMimeExt": "mp4v-es", "size": len("mp4v-es"), "pMimeType": mime_type_video_mpeg4},
        {"type": 3, "pMimeExt": "3gp", "size": len("3gp"), "pMimeType": mime_type_video_3gpp},
        {"type": -1, "pMimeExt": None, "size": 0, "pMimeType": None}
    ]
    
    @staticmethod
    def convertMimeType(mimeType):
        result = mimeType
        pMimeType = mimeType
        if pMimeType is not None:
            if pMimeType.startswith(MimeTypeUtil.mime_group_audio) or pMimeType.startswith(MimeTypeUtil.mime_group_video):
                pGroup = next((group for group in MimeTypeUtil.mimeGroup if pMimeType.startswith(group["pGroup"])), None)
                if pGroup is not None:
                    pMimeItem = next((item for item in MimeTypeUtil.mimeTypeList if item["type"] == pGroup["type"] and len(pMimeType[pGroup["size"]:]) == item["size"] and pMimeType[pGroup["size"]:] == item["pMimeExt"]), None)
                    if pMimeItem is not None:
                        result = pMimeItem["pMimeType"]
            else:
                result = MimeTypeUtil.mime_type_unsupported
            logging.debug("convertMimeType got mimetype %s, converted into mimetype %s", pMimeType, result)
        return result