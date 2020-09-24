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
            sub_category_id  = request.GET.get('sub_category_id') 
            color_filter     = request.GET.getlist('color')
            silouette_filter = request.GET.getlist('silouette') 
            size_filter      =  request.GET.getlist('size') 

            sub_category     = SubCategory.objects.prefetch_related(
                                        'product_set__series', 
                                        'product_set__color__filtering_color', 
                                        'product_set__promotion').get(id = sub_category_id)
                
            if Promotion.objects.filter(name = sub_category.name).exists():          
                products     = Promotion.objects.get(name = sub_category.name).product_set.all()
            elif sub_category.product_set.exists():
                products     = sub_category.product_set.all()
            else:
                products     = Product.objects.all()   
            
            products         = products.filter(color__filtering_color__name__in = color_filter) if color_filter else products
            products         = products.filter(silouette__name__in = silouette_filter) if silouette_filter else products
            products         = products.filter(size__name__in = size_filter) if size_filter else products
        
        except:
            return JsonResponse({'message':'INVALID_VALU'}, status= 401)
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

