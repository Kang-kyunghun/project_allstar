import json

from django.views       import View
from django.http        import JsonResponse
from django.db.models   import Prefetch

from account.models     import Wishlist
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

class SearchView(View):
    def get(self, request):
        products_list = [{
                    'id'    : product.id ,
                    'name'  : product.series.name ,
                    'image' : product.main_image,
                }for product in Product.objects.all()]
        
        return JsonResponse({'products': products_list}, status=200)

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
            return JsonResponse({'message':'INVALID_VALUE'}, status= 401)
        else:
            products_list=[{
                "main_image":{
                        'id'          : product.id,
                        'price'       : int(product.price),
                        'image_url'   : [product.main_image, product.hover_image],
                        'series_name' : product.series.name,
                        'discout_rate': int(product.discount_rate) if product.discount_rate else None,
                        'whishlist'   : is_wishlist(request, product.id)
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
        RECOMMENDATIONS = 10  
        try:
            queryset = Product.objects.all()
            product = queryset.select_related('sex', 'color', 'sub_category', 'series', 'promotion', 'productinformation')\
                .prefetch_related('medium_set', 'size').get(id=id)
        except:
            return JsonResponse({'message':"INVALID_PRODUCT"}, status=400)

        information_dict = {
        'is_wishlist'           : is_wishlist(request, id),
        'price'                 : int(product.price),
        'discount_rate'         : int(product.discount_rate) if product.discount_rate else None,
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
        'size_range'            : '{}-{}'\
            .format(product.productinformation.minimum_size, product.productinformation.maximum_size),
        'promotion'             : product.promotion.name if product.promotion else None,
        'sub_images'            : [
                {
                    'medium_url'        : product_medium.medium_url,
                    'medium_type'       : product_medium.medium_type
                } for product_medium in product.medium_set.all()],
        'size_list'             : [size.name for size in product.size.order_by('name')],
        'related_products'      : [
                {
                        'id'            : series_product.id,
                        'main_image'    : series_product.medium_set.all()[3].medium_url 
                } for series_product in queryset.filter(series_id=product.series)],
        'recommended_products'  : [
                {
                    'main_image'        :similar_product.main_image,
                    'hover_image'       :similar_product.hover_image,
                    'serial_number'     :similar_product.serial_number,
                    'promotion'         :similar_product.promotion.name if similar_product.promotion else None
                } for similar_product in queryset.exclude(id=id).filter(price=product.price)[:RECOMMENDATIONS]],
        }
        return JsonResponse({'product_information': [information_dict]}, status=200)