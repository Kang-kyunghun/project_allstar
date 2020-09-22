import json

from django.http        import JsonResponse
from django.views       import View
from django.db.models   import Prefetch

from account.models     import Wishlist
from .models            import (FilteringColor, 
                                Product, 
                                SubCategory, 
                                Series, 
                                Sex, 
                                Color, 
                                ProductSize, 
                                Size, 
                                Medium, 
                                ProductInformation, 
                                Promotion)

class ProductView(View):
    @is_product_wishlist
    def get(self, request, id):  
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return JsonResponse({'message':"INVALID_PRODUCT"}, status=400)

        information_dict = {}
        information_dict['is_wishlist']         = request.is_wishlist        
        information_dict['price']               = int(product.price)
        information_dict['discount_rate']       = product.discount_rate
        information_dict['simple_description']  = product.simple_description
        information_dict['serial_number']       = product.serial_number
        information_dict['main_image']          = product.main_image
        information_dict['sex']                 = product.sex.name
        information_dict['color']               = product.color.name
        information_dict['sub_category']        = product.sub_category.name

        product = Product.objects.filter(id=id).select_related('series')[0]
        information_dict['series_name']         = product.series.name
        information_dict['detail_description']  = product.series.detail_description
        information_dict['features']            = product.series.feature
        information_dict['series_sub_image']    = product.series.additional_image 
        information_dict['series_image']        = product.series.image 
        information_dict['related_products']    = [{
            'serial_number'    : series_product.serial_number,
            'main_image'       : Medium.objects.filter(product_id=series_product.id)[3].medium_url
            } for series_product in Product.objects.filter(series_id=product.series)]
        information_dict['sub_images']          = [{
            'medium_url'    : i.medium_url,
            'medium_type'   : i.medium_type} 
            for i in Medium.objects.filter(product=id)]

        product_information                     = ProductInformation.objects.get(product_id=id)
        information_dict['material']            = product_information.material
        information_dict['manufacturer']        = product_information.manufacturer
        information_dict['country']             = product_information.country
        information_dict['caution']             = product_information.caution
        information_dict['assurance']           = product_information.quality_assurance
        information_dict['as_center']           = product_information.as_center
        information_dict['manufacture_date']    = product_information.manufacture_date

        try: 
            if product.promotion.name:
                information_dict['promotion']   = product.promotion.name
        except AttributeError:
            information_dict['promotion']       = None

        size_ids = ProductSize.objects.filter(product_id = id)
        size_list = sorted([size_id.size.name for size_id in size_ids])
        information_dict['size_list']         = size_list
        information_dict['size_range']        = str(size_list[0])+' - '+str(size_list[-1])

        recommendations = Product.objects.filter(sex=product.sex, price=product.price).prefetch_related('promotion')[0:10]
        try:
            recommended_products = [
                {'main_image':recommendation.main_image,
                'hover_image':recommendation.hover_image,
                'serial_number':recommendation.serial_number,
                'promotion':recommendation.promotion.name} for recommendation in recommendations
                ]
        except AttributeError:
            recommended_products = [
                {'main_image':recommendation.main_image,
                'hover_image':recommendation.hover_image,
                'serial_number':recommendation.serial_number,
                'promotion':None}  for recommendation in recommendations
                ]
        information_dict['recommended_product'] = recommended_products
        
        return JsonResponse({'product_information': [information_dict]}, status=200)