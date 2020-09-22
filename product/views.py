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
    
class ListView(View):   
    def get(self, request, sub_category_id):
        
        try:
            sub_category             = SubCategory.objects.get(id =  sub_category_id)
        except:
            return JsonResponse({'message':'INVALID_VALUE'}, status= 401)
        else:
            if sub_category.name == '전체보기':
                products             = Product.objects.all()
            elif sub_category.name in ['베스트셀러', 'MEMBERS ONLY', 'SALE'] :          
                products =Promotion.objects.get(name = sub_category.name).product_set.all()
            else:
                products = sub_category.product_set.all()
            
            products_list             =[]
            for product in products:
                color_products_list   = []
                series_id             = product.series.id
                color_products        = Product.objects.filter(series_id = series_id)
                
                for color_product in color_products:
                    color_products_list.append({
                            'id'          : color_product.id,
                            'image_url'   : [color_product.main_image, color_product.hover_image],
                            'color'       : color_product.color.filtering_color.name
                    }) 
                
                products_list.append({
                    "main_image":{
                            'id'          : product.id,
                            'price'       : int(product.price),
                            'image_url'   : [product.main_image, product.hover_image],
                            'series_name' : product.series.name
                        },
                    "color_image" : color_products_list
                })
        
            return JsonResponse({'products': products_list}, status=200)

