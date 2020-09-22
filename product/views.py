import json

from django.views   import View
from django.http    import JsonResponse

from .models        import (Category, 
                            SubCategory, 
                            Series, 
                            Sex, 
                            FilteringColor, 
                            Color, 
                            Promotion, 
                            Silouette, 
                            Size, 
                            Product, 
                            Medium, 
                            ProductInformation, 
                            ProductSize )
    
class MainView(View):
    def get(self, request):
        sub_category_list = [{
                'id'   : sub_category.id,
                'name' : sub_category.name
        } for sub_category in SubCategory.objects.all()]

        return JsonResponse({'sub_categories': sub_category_list}, status=200)

class ListView(View):   
    def get(self, request):
        try:
            sub_category_id    = request.GET.get('sub_category_id', None) 
            if sub_category_id == None:
                products       = Product.objects.all()
            else:
                sub_category   = SubCategory.objects.prefetch_related('product_set__series', 'product_set__color__filtering_color', 'product_set__promotion').get(id =  sub_category_id)
                
                if Promotion.objects.filter(name = sub_category.name) :          
                    products   = Promotion.objects.get(name = sub_category.name).product_set.all()
                else:
                    products   = sub_category.product_set.all()      
        except:
            return JsonResponse({'message':'INVALID_VALUE'}, status= 401)
        else:
            products_list=[{
                "main_image":{
                        'id'          : product.id,
                        'price'       : int(product.price),
                        'image_url'   : [product.main_image, product.hover_image],
                        'series_name' : product.series.name
                    },

                "color_image" : [{
                        'id'          : color_product.id,
                        'image_url'   : [color_product.main_image, color_product.hover_image],
                        'color'       : color_product.color.filtering_color.name
            }  for color_product in Product.objects.filter(series_id = product.series.id)]
            } for product in products]
    
        return JsonResponse({'products': products_list}, status=200)

