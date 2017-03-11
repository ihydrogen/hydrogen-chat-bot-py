import json

import vk

import vk
import vk_api
import vk_auth.auth


def authorize(username=None, password=None, type=None):
    if username is None:
        username = input("Enter your username: ")
    if password is None:
        password = input("Enter your password: ")

    au = vk_auth.auth.VKAuth(username, password, authtype=type)
    auth_try(au)


def auth_try(au):
    try:
        auth_result = au.authorize()
        print("Auth complete. token: " + auth_result.access_token)
        print("Getting user data...")
        vkapi = vk.API(vk.Session(auth_result.access_token))
        from vk_api import api

        json_ = str(vkapi   .users.get(v="5.35")[0]).replace("'", '"')
        print(json_)
        user = json.loads(json_, object_hook=api.User.from_json)

        acc = api.Account()
        acc.token = auth_result.access_token
        acc.first_name = user.first_name
        acc.last_name = user.last_name
        acc.user_id = user.id


        # Saving result account
        from vk_auth import account_manager
        acc_mgr = account_manager.AccountManager()
        acc_mgr.add_account(acc)
        print("OK")
    except vk_auth.auth.VKAuth.AuthException as exc:
        # Invalid uname or passwd
        if exc.error == 'invalid_client':
            # Print message 4 user
            print("Invalid username or password. Try to LogIn again:)")
            # Ask uname and passwd again
            authorize()
        elif exc.error == 'need_validation':
            # Two factor Auth required
            print("Need to conform you own this account!")
            print("The validation method is %s" % (str(au.two_factor_object.two_factor_method)))
            print(
                "Enter code (or -s to send sms message to %s) to authorize" % au.two_factor_object.two_factor_phone_number)
            code = input("Verification code: ")
            # Ask user for SMS code sending
            if code == '-s' and (input("Send SMS Message? [Y/M]: ").lower() == 'y'):
                print("Trying verification through sms message...")
                # Repeat auth request with FORCE sms send parameter
                au.fsms(True)
                au.update()
                auth_try(au)
                pass
            # Repeat auth request with code of two factor authorization
            au.with_two_factor_code(code)
            au.update()
            auth_try(au)
        elif exc.error == "need_captcha":
            # Process captcha request
            code = input("You need to enter code from this image: %s\nCode: " % au.captcha_object.captcha_url)
            print("Trying with %s..." % code)
            au.with_captcha(code)
            au.update()
            auth_try(au)

