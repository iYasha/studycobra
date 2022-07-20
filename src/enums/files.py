from enum import Enum


class FileType(str, Enum):
    MP3_AUDIO = 'audio/mpeg'
    MP4_VIDEO = 'video/mp4'
    IMAGE_JPG = 'image/jpeg'
    IMAGE_PNG = 'image/png'
