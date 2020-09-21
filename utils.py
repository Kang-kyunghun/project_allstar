import json 
import jwt

from django.http        import JsonResponse

from Allstar.settings   import SECRET_KEY, ALGORITHM

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.header.keys('Authorization'): 
            return JsonResponse({'message':'NO_TOKEN'}, status=403)
        token = request.header['Authorized']

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
            request.account_id = decoded_token['account_id']
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message':'INVALID_TOKEN'}, status=403)

        return func(self, request, *args, **kwargs) 

    return wrapper