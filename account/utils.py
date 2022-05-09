# from account.serializers import *
# #
# #
# # def my_jwt_response_handler(token, user=None, request=None):
# #     return {
# #         'token': token,
# #         'user': UserLoginSerializer(user, context={'request': request}).data
# #     }
# # from datetime datetime datetime
# from calendar import timegm
# from rest_framework_jwt.settings import api_settings
#
# def jwt_payload_handler(user):
#     """ Custom payload handler
#     Token encrypts the dictionary returned by this function, and can be decoded by rest_framework_jwt.utils.jwt_decode_handler
#     """
#     return {
#         'mobile': user.mobile,
#         'otp': user.otp,
#         'country_code': user.country_code,
#
#         # 'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
#         # 'orig_iat': timegm(
#         #     datetime.utcnow().utctimetuple()
#         # )
#     }
#
# def jwt_response_payload_handler(token, user=None, request=None):
#     """ Custom response payload handler.
#
#     This function controlls the custom payload after login or token refresh. This data is returned through the web API.
#     """
#     return {
#         'token': token,
#         'user': {
#              'mobile': user.mobile,
#             'otp': user.otp,
#             'country_code': user.country_code,
#         }
#     }


import datetime
import jwt
from django.conf import settings


def generate_access_token(user):

    access_token_payload = {
        'user_mobile': user.mobile,
        'user_otp': user.otp,
        'user_country_code': user.country_code,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        # 'user_id' : user.id,
        'user_mobile': user.mobile,
        'user_otp': user.otp,
        'user_country_code': user.country_code,

        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token
