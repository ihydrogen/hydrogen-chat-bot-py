from bot_header import *
from vk_auth.vk_app import VKApp
import vk_auth.vk_2fa_type

# @__url__ Basic VK Direct auth url
###
# 2FA APP:
# client_id - SPECIFIC VK APPLICATION ID
# client_secret - SECRET KEY OF SPECIFIC VK APPLICATION
# /2FA APP
# USERDATA:
# username - EMAIL OR PHONE NUMBER OF USER
# password - ACCOUNT PASSWORD OF USER
# /USERDATA
# scrope - VK TOKEN PRIVILEGES e.g manipulate with audio list, friends, videos, etc...
# 2fa_supported - FLAG THAT ENABLES TWO FACTOR AUTH SUPPORT (sms to phone or auth app code)
# force_sms - IF 2FA - SEND SMS TO PHONE PRIMARY
###
__url__ = "https://oauth.vk.com/token?" \
          "grant_type=password&client_id=%s" \
          "&client_secret=%s" \
          "&username=%s&password=%s" \
          "&scrope=%s&2fa_supported=1" \
          "&force_sms=%s"

# class describes result of authorization
class AuthResult:
    access_token = ''
    trusted_hash = ''
    uid = ''

# class describe two factor auth fields
class TwoFactorObject:
    two_factor_code = ''
    two_factor_phone_number = ''
    two_factor_method = None

# class describe captcha fields
class CaptchaObject:
    captcha_code = ''
    captcha_url = ''
    captcha_sid = ''

    # format id of captcha image and value from user to string
    def format(self):
        return "&captcha_sid=%s&captcha_key=%s" % (self.captcha_sid, self.captcha_code)

# class describe user auth required fields
class UserData:
    password = ''
    username = ''

# Main VKAuth class implements vk_auth authorization
class VKAuth():


    # str.split()
    ######################
    __client_id__ = ''
    __client_secret__ = ''
    __request_url__ = ''
    ######################

    # VK App e.g. Apple client or Android client or windows desktop
    auth_type = VKApp.WIN

    # scrope (DESCRIBED ABOVE)

    prevs = ''

    # DESCRIBED ABOVE
    user_data = None

    captcha_object = None
    two_factor_object = None

    # DESCRIBED ABOVE
    force_sms = '0'

    # INITIALIZE VARIABLES
    def __init__(self, username, password, authtype=VKApp.WIN, prevs='audio,wall,friends,messages,status'):
        username = username.strip()
        password = password.strip()
        if not username or not password:
            raise AttributeError("Invalid username or password argument (u:'%s', p:'%s')" % (username, password))
        self.user_data = UserData()
        self.user_data.username = username
        self.user_data.password = password
        self.auth_type = authtype
        self.prevs = prevs

    # SET FORCE SMS FLAG
    def fsms(self, fsms):
        if fsms:
            self.force_sms = '1'
        else:
            self.force_sms = '0'

    # VK AUTH EXCEPTION e.g. invalid client or captcha needed
    class AuthException(Exception):
        error = ''
        error_description = ''

        def __init__(self, error, error_description):
            self.error = error
            self.error_description = error_description


    # format basic url (__url__)
    def __make_request__(self, sms=force_sms):
        self.__request_url__ = __url__ % (
              self.__client_id__,
              self.__client_secret__,
              self.user_data.username, self.user_data.password, self.prevs, sms)
        if self.two_factor_object is not None and self.two_factor_object.two_factor_code:
            self.__request_url__ += "&code=%s" % (self.two_factor_object.two_factor_code)
        if self.captcha_object is not None and self.captcha_object.captcha_code:
            self.__request_url__ += self.captcha_object.format()


    # init __client_id__ and __client_secret__
    def __auth_type__(self):
        if self.auth_type is not None:
            self.__client_id__ = self.auth_type.value.cid
            self.__client_secret__ = self.auth_type.value.sec
        else:
            print("Trying with default app")
            self.__client_id__ = VKApp.WIN.value.cid
            self.__client_secret__ = VKApp.WIN.value.secq

    # send HTTPS request to vk_auth api and parse response with json.loads()
    def __do_auth__(self):
        url = self.__request_url__
        response = requests.get(url).text
        return json.loads(str(response))

    # append code of tfactor auth to request
    def with_two_factor_code(self, code):
        self.two_factor_object.two_factor_code = code

    # append captcha data to request
    def with_captcha(self, cap):
        self.captcha_object.captcha_code = cap

    def update(self):
        self.__request_url__ = ''

    def authorize(self):
        # parsing client id and secret
        self.__auth_type__()

        # Make request url if it dont exists
        if not self.__request_url__:
            self.__make_request__(self.force_sms)

        # Getting response from vk_auth api on JSON format
        json_object = self.__do_auth__()

        # Checking response for errors
        if 'error' in json_object:
            if 'error_description' in json_object:
                desc = json_object['error_description']
            else:
                desc = ''

            # process need_validation error
            if json_object['error'] == 'need_validation':
                self.two_factor_object = TwoFactorObject()
                self.two_factor_object.two_factor_method = vk_auth.vk_2fa_type.parse_validation_method(json_object['validation_type'])
                self.two_factor_object.two_factor_phone_number = json_object['phone_mask']
            # processing need_captcha error
            elif json_object['error'] == 'need_captcha':
                self.captcha_object = CaptchaObject()
                self.captcha_object.captcha_sid = json_object['captcha_sid']
                self.captcha_object.captcha_url = json_object['captcha_img']

            # creating :Exception class and throwing it.
            raise self.AuthException(json_object['error'], desc)

        # checking for auth success
        elif 'access_token' in json_object:
            # parsing data from server response
            r = AuthResult()
            r.access_token = json_object['access_token']
            if 'trusted_hash' in json_object:
                r.trusted_hash = json_object['trusted_hash']
            if 'user_id' in json_object:
                r.uid = json_object['user_id']
            return r

        return None















