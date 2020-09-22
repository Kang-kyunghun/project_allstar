import json 
import jwt

from django.http        import JsonResponse

from Allstar.settings   import SECRET_KEY, ALGORITHM
from account.models     import Wishlist

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

def is_product_wishlist(func):
    def wrapper(self, request, id, *args, **kwargs):
        global is_wishlist
        is_wishlist = False
        try:
            token = request.headers['Authorization']
            decoded_token = jwt.decode(token, SECRET_KEY, ALGORITHM)
            request.account_id = decoded_token['account_id']
            if Wishlist.objects.filter(product_id=id, account_id=request.account_id).exists():
                is_wishlist = True
        except jwt.exceptions.DecodeError:
            pass
        except KeyError:
            pass
        request.is_wishlist = is_wishlist
        return func(self, request, id, *args, **kwargs)
    return wrapper