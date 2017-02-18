import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from vk_auth.auth import *

au = VKAuth("example", "example")

try:
    au.authorize()
except VKAuth.AuthException as e:
    assert e.error == 'invalid_client' or e.error == 'need_captcha'
    pass
