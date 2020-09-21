import json
import bcrypt
import jwt
import re
import datetime
from Allstar.settings   import SECRET_KEY, ALGORITHM
from django.http        import JsonResponse
from django.views       import View
from .models            import Account, Wishlist
from utils             import login_required
from product.models     import Product

class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)

        # 필수정보 입력여부 확인
        if not (
            'email'                     in data.keys()
            and 'name'                  in data.keys()
            and 'phone_number'          in data.keys()
            and 'date_of_birth'         in data.keys()
            and 'password'              in data.keys()
            and 'is_male'               in data.keys()
            # and 'is_agreed_texting'     in data.keys() # 프론트엔드 요청으로, 백엔드에서 True/False 임의로 저장
            # and 'is_agreed_emailing'    in data.keys() # 프론트엔드 요청으로, 백엔드에서 True/False 임의로 저장
            ):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        # email validation
        if "@" not in data['email'] or "." not in data['email']:
            return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

        # phone_number validation
        if not re.fullmatch("^010(\d){8}$", data['phone_number']):
            return JsonResponse({'message':'WRONG_NUMBER'}, status=401)

        # date_of_birth validation
        try:
            datetime.datetime.strptime(data['date_of_birth'], '%Y%m%d')
            YYYY_MM_DD = "{}-{}-{}". format(data['date_of_birth'][:4], data['date_of_birth'][4:6], data['date_of_birth'][6:8])
        except ValueError:
            return JsonResponse({'message':'INCORRECT_BIRTHDAY'}, status=401)

        # password validation (숫자/대소문자/길이/특수문자)
        if not re.fullmatch("(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#$%]).{8,16}$", data['password']):
            return JsonResponse({'message':'INVALID_PASSWORD'}, status=400)

        # 중복가입 방지 (전화번호, 이메일)
        if (
            Account.objects.filter(phone_number = data['phone_number']) 
            or 
            Account.objects.filter(email = data['email'])
            ):
            return JsonResponse({'message':'DUPLICATED_USER'}, status=401)

        if data['is_male'] == True:
            sex_value = '남'
        else:
            sex_value = '여'

        # 회원정보 생성
        Account(
    	    email               = data['email'],
            name    		    = data['name'],
        	phone_number        = data['phone_number'],
            date_of_birth       = YYYY_MM_DD,
            sex                 = sex_value,
            password            = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_agreed_emailing  = True, # 프론트엔드 요청으로, 백엔드에서 True/False 임의로 저장
            is_agreed_texting   = False, # 프론트엔드 요청으로, 백엔드에서 True/False 임의로 저장
        ).save()
        return JsonResponse({'message':'SUCCESS'}, status=200)
        
class SignInView(View):
    def post(self, request):           
        data = json.loads(request.body)

        # 이메일 미입력    
        if not data.get('email'):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        # 비밀번호 미입력
        if not data.get('password'):
            return JsonResponse({'message':'KEY_ERROR'}, status=400)       

        # 없는 이메일
        if not Account.objects.filter(email=data['email']):
            return JsonResponse({'message':'INVALID_USER'}, status=400)
       
        # 비밀번호 틀림
        if not bcrypt.checkpw(data['password'].encode('utf-8'), Account.objects.get(email = data['email']).password.encode('utf-8')):
            return JsonResponse({'message':'INVALID_USER'}, status=401)

        # 입력한 이메일과 비밀번호 일치하면 성공 - 토큰발행
        accessed_user   = Account.objects.get(email=data['email'])
        access_token = jwt.encode({'account_id': accessed_user.id}, SECRET_KEY, ALGORITHM)
        return JsonResponse({'Authorization': access_token.decode('utf-8')}, status=200)
        
class WishlistView(View):
    @login_required
    def post(self, request): # wishlist 추가/삭제
        data = json.loads(request.body)
        if not 'product_id' in data.keys(): 
            return JsonResponse({'message':'KEY_ERROR'}, status=401)

        if not Product.objects.filter(serial_number=data['serial_number']): 
            return JsonResponse({'message':'INVALID_PRODUCT_ID'}, status=400)

        product_id = Product.objects.get(serial_number=data['serial_number']).id
        if Wishlist.objects.filter(product_id = product_id, account_id=request.account_id): #위시리스트에 이미 있는 경우 삭제
            Wishlist.objects.get(product_id=product_id, account_id=1).delete()
            return JsonResponse({'message':'DELETED'}, status=200)

        Wishlist.objects.create(product_id=product_id, account_id=request.account_id) # 위시리스트에 없는 경우 생성
        return JsonResponse({'message':'ADDED'})

    @login_required
    def get(self, request): # wishlist 보기
        data = json.loads(request.body)
        wishitems = Wishlist.objects.filter(account_id=request.account_id)
        wishitems_list = []
        for wishitem in wishitems:
            wish_product = wishitem.product
            temp_dict = {}
            temp_dict['main_image']     = wish_product.main_image
            temp_dict['price']          = wish_product.price
            temp_dict['serial_number']  = wish_product.serial_number
            temp_dict['series_name']    = wish_product.series.name
            wishitems_list.append(temp_dict)

        return JsonResponse({'wishlist':wishitems_list}, status=200)