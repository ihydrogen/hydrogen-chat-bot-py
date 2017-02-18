from enum import Enum

# VK TWO FACTOR AUTH TYPE
class VKAuthApp(Enum):
    APP = 0
    SMS = 1


def parse_validation_method(param):
    if param == '2fa_app':
        return VKAuthApp.APP
    else:
        return VKAuthApp.SMS