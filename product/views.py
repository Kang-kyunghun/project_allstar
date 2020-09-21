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
    
class MainListView(View):   
    def get(self, request):
        products_list =[]
        products                   = Product.objects.all()
        for product in products:
            serial_number          = product.serial_number
            price                  = product.price
            main_image             = product.main_image
            hover_image            = product.hover_image
            series_name            = Series.objects.get(id = product.series_id).name
            image                  = [main_image, hover_image] 
            series_id              = Series.objects.get(id = product.series_id).id
            globals()[f'main{product.id}'] ={
                    'id'           : serial_number,
                    'price'        : int(price),
                    'image_url'    : image,
                    'series_name'  : series_name
            }

            color_products_list    = []
            color_products         = Product.objects.filter(series_id = series_id)
            for color_product in color_products:
                serial_number      = color_product.serial_number
                main_image         = color_product.main_image
                hover_image        = color_product.hover_image
                image              = [main_image, hover_image]
                filter_color_id    = Color.objects.get(id=color_product.color_id).filtering_color_id
                filter_color       = FilteringColor.objects.get(id= filter_color_id).name
                color_products_list.append({
                        'id'        : serial_number,
                        'image_url' : image,
                        'color'     : filter_color
                })          
    
            products_list.append({
                "main_image"  : globals()[f'main{product.id}'],
                "color_image" : color_products_list
            })
        return JsonResponse({'products': products_list}, status=200)

class Chuck70ListView(View):   
    def get(self, request):
        products_list =[]
        sub_category_id            =SubCategory.objects.get(name ='척 70')
        products                   = Product.objects.filter(sub_category_id = sub_category_id)
        for product in products:
            serial_number          = product.serial_number
            price                  = product.price
            main_image             = product.main_image
            hover_image            = product.hover_image
            series_name            = Series.objects.get(id = product.series_id).name
            image                  = [main_image, hover_image] 
            series_id              = Series.objects.get(id = product.series_id).id
            globals()[f'main{product.id}'] ={
                    'id'           : serial_number,
                    'price'        : int(price),
                    'image_url'    : image,
                    'series_name'  : series_name
            }

            color_products_list    = []
            color_products         = Product.objects.filter(series_id = series_id)
            for color_product in color_products:
                serial_number      = color_product.serial_number
                main_image         = color_product.main_image
                hover_image        = color_product.hover_image
                image              = [main_image, hover_image]
                filter_color_id    = Color.objects.get(id=color_product.color_id).filtering_color_id
                filter_color       = FilteringColor.objects.get(id= filter_color_id).name
                color_products_list.append({
                        'id'        : serial_number,
                        'image_url' : image,
                        'color'     : filter_color
                })          
    
            products_list.append({
                "main_image"  : globals()[f'main{product.id}'],
                "color_image" : color_products_list
            })
        return JsonResponse({'products': products_list}, status=200)
