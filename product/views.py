import json

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Prefetch

from utils              import is_wishlist
from .models            import (Category, 
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
                                ProductSize)
    
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

class ProductView(View):
    def get(self, request, id):  
        try:
            queryset = Product.objects.select_related('sex', 'color', 'sub_category', 'series', 'promotion', 'productinformation')\
                .prefetch_related('medium_set', 'size')
            product = queryset.get(id=id)
        except:
            return JsonResponse({'message':"INVALID_PRODUCT"}, status=400)

        information_dict = {
        'is_wishlist'           : is_wishlist(request, id),
        'price'                 : int(product.price),
        'discount_rate'         : product.discount_rate,
        'simple_description'    : product.simple_description,
        'serial_number'         : product.serial_number,
        'main_image'            : product.main_image,
        'sex'                   : product.sex.name,
        'color'                 : product.color.name,
        'sub_category'          : product.sub_category.name,
        'series_name'           : product.series.name,
        'detail_description'    : product.series.detail_description,
        'features'              : product.series.feature,
        'series_sub_image'      : product.series.additional_image,
        'series_image'          : product.series.image,
        'material'              : product.productinformation.material,
        'manufacturer'          : product.productinformation.manufacturer,
        'country'               : product.productinformation.country,
        'caution'               : product.productinformation.caution,
        'assurance'             : product.productinformation.quality_assurance,
        'as_center'             : product.productinformation.as_center,
        'manufacture_date'      : product.productinformation.manufacture_date,
            'related_products'      : [{
            'id'            : series_product.id,
            'main_image'    : series_product.medium_set.all()[3].medium_url 
            } for series_product in queryset.filter(series_id=product.series)], 
        'sub_images'            : [{
            'medium_url'    : product_medium.medium_url,
            'medium_type'   : product_medium.medium_type} 
            for product_medium in product.medium_set.all()]}

        try: 
            if product.promotion.name:
                information_dict['promotion']   = product.promotion.name
        except AttributeError:
            information_dict['promotion']       = None

        size_ids = ProductSize.objects.filter(product_id = id)
        size_list = sorted([size_id.size.name for size_id in size_ids])
        information_dict['size_list']           = size_list
        information_dict['size_range']          = '{}-{}'\
            .format(product.productinformation.minimum_size, product.productinformation.maximum_size)


        similar_products = queryset.exclude(id=id).filter(price=product.price)[0:10]
        try:
            recommended_products = [
                {'main_image'   :similar_product.main_image,
                'hover_image'   :similar_product.hover_image,
                'id'            :similar_product.id,
                'promotion'     :similar_product.promotion.name} for similar_product in similar_products
                ]
        except AttributeError:
            recommended_products = [
                {'main_image':similar_product.main_image,
                'hover_image':similar_product.hover_image,
                'serial_number':similar_product.serial_number,
                'promotion':None}  for similar_product in similar_products
                ]
        information_dict['recommended_product'] = recommended_products
        
        return JsonResponse({'product_information': [information_dict]}, status=200)