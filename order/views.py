import json

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Prefetch

from utils                  import login_required, is_wishlist
from .models                import Cart
from account.models         import Account, Wishlist
from product.models         import (FilteringColor, 
                                    Product, 
                                    Series, 
                                    Color, 
                                    Size, 
                                    Medium, 
                                    Promotion)

class CartView(View):
    @login_required 
    def get(self, request):
        items = [{
            'buy_now'               : item.buy_now,
            'quantity'              : item.quantity,
            'cart_id'               : item.id,
            'is_wishlist'           : is_wishlist(request, item.id),
            'size'                  : item.size.name,
            'id'                    : item.product.id,
            'main_image'            : item.product.main_image,
            'color'                 : item.product.color.name,
            'price'                 : int(item.product.price),
            'discount_rate'         : int(item.product.discount_rate) if item.product.discount_rate else None,
            'series_name'           : item.product.series.name,
            } for item in Cart.objects.filter(account_id=request.account_id).select_related('product__series')]
                    
        return JsonResponse({'cart_list':items}, status=200)

    @login_required
    def patch(self, request):
        data = json.loads(request.body)
        try:
            cart = Cart.objects.get(id=data['cart_id'])
            if (
                'quantity_change' in data.keys()
                and 'buy_now' in data.keys()
                ):
                return JsonResponse({'message':'KEY_ERROR'}, status=400)
            elif 'buy_now' in data.keys():
                cart.buy_now = not cart.buy_now
                cart.save()
                return JsonResponse({'message':"BUY_NOW_MODIFIED"}, status=201)
            elif (
                'quantity_change' in data.keys()
                and cart.buy_now == False
                ):
                cart.quantity += int(data['quantity_change'])
                if 0 < cart.quantity <= 5:
                    cart.save()
                    return JsonResponse({'message':"QUANTITY_MODIFIED"}, status=201)
                return JsonResponse({'message':"QUANTITY_ERROR"}, status=400)
            return JsonResponse({'message':'KEY_ERROR'}, status=400)  
        except:
            return JsonResponse({'message':"KEY_ERROR"}, status=400)
    @login_required
    def post(self, request):
        try:
            data               = json.loads(request.body)
            size_id            = Size.objects.get(name=data['size']).id
            Cart.objects.create(
                account_id     = request.account_id,
                product_id     = data['product_id'],  
                size_id        = size_id,
                quantity       = data['quantity']
            )
            return JsonResponse({'sub_categories': 'post'}, status=200)
        
        except KeyError:
            return JsonResponse({'message':'Key Error'}, status=401)
    
    @login_required
    def delete(self, request, cart_id=0):
        cart    = Cart.objects.filter(buy_now = False, account_id = request.account_id)
        if cart_id == 0:
            cart.delete()
        else:
            try:
                cart.get(id = cart_id).delete()
            except:
                return JsonResponse({'message':'This product is not in cart'}, status=400)
        return JsonResponse({'message':'SUCCESS'}, status=200)