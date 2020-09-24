import json
import bcrypt
import jwt
import re
import datetime

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Q, Prefetch

from Allstar.settings   import SECRET_KEY, ALGORITHM
from utils              import login_required
from product.models     import Product
from .models            import Account, Wishlist

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if ("@" not in data['email'] or "." not in data['email'] or
                not re.fullmatch("^010(\d){8}$", data['phone_number']) or
                not re.fullmatch("(?=.*?[A-Za-z])(?=.*?[0-9])(?=.*?[!@#$%]).{8,16}$", data['password'])):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=401)

            try:
                datetime.datetime.strptime(data['date_of_birth'], '%Y%m%d')
                YYYY_MM_DD = "{}-{}-{}". format(
                    data['date_of_birth'][:4], data['date_of_birth'][4:6], data['date_of_birth'][6:8])
            except ValueError:
                return JsonResponse({'message':'INCORRECT_BIRTHDAY'}, status=401)

            if Account.objects.filter(
                Q(phone_number=data['phone_number']) | Q(email=data['email'])
            ).exists():
                return JsonResponse({'message':'DUPLICATED_USER'}, status=401)

            Account (
                email               = data['email'],
                name    		    = data['name'],
                phone_number        = data['phone_number'],
                date_of_birth       = YYYY_MM_DD,
                sex                 = '남' if data['is_male'] == True else '여',
                password            = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                is_agreed_emailing  = True,
                is_agreed_texting   = False,
            ).save()
            return JsonResponse({'message':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
class SignInView(View):
    def post(self, request):           
        data = json.loads(request.body)
        try:
            if not Account.objects.filter(email=data['email']):
                return JsonResponse({'message':'INVALID_USER'}, status=400)

            if not bcrypt.checkpw(
                data['password'].encode('utf-8'), Account.objects.get(email=data['email']).password.encode('utf-8')):                
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            accessed_user   = Account.objects.get(email=data['email'])
            access_token = jwt.encode({'account_id': accessed_user.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'Authorization': access_token.decode('utf-8')}, status=200)
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
class WishlistView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)
        if not 'id' in data.keys(): 
            return JsonResponse({'message':'KEY_ERROR'}, status=401)

        if not Product.objects.filter(id=data['id']).exists(): 
            return JsonResponse({'message':'INVALID_PRODUCT_NUMBER'}, status=400)

        if Wishlist.objects.filter(product_id = data['id'], account_id=request.account_id): 
            Wishlist.objects.get(product_id=data['id'], account_id=request.account_id).delete()
            return JsonResponse({'message':'DELETED'}, status=200)

        Wishlist.objects.create(product_id=data['id'], account_id=request.account_id) 
        return JsonResponse({'message':'ADDED'}, status=200)

    @login_required
    def get(self, request):
        wishitems = Wishlist.objects.filter(account_id=request.account_id).prefetch_related('product')
        wish_items = [
            {'main_image'   :wishitem.product.main_image, 
            'price'         :int(wishitem.product.price), 
            'series_name'   :wishitem.product.series.name,
            'discount_rate' :wishitem.product.discount_rate, 
            'id'            :wishitem.product.id} for wishitem in wishitems]
        
        return JsonResponse({'wishlist':wish_items}, status=200)
