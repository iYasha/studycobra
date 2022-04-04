import enum


class PlatformType(str, enum.Enum):
    IOS = 'IOS'
    ANDROID = 'ANDROID'
    WEB = 'WEB'
