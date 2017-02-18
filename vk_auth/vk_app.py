from enum import Enum


class VKApp(Enum):
    # subclass describes vk_auth app
    class app:
        cid = ''
        sec = ''

        def __init__(self, cid, sec):
            self.cid = cid
            self.sec = sec

    APPLE_IPHONE = app("3140623", "VeWdmVclDCtn6ihuP1nt")
    WIN = app("3697615", "AlVXZFMUqyrnABp8ncuU")
    ANDROID = app("2274003", "hHbZxrka2uZ6jB1inYsH")

