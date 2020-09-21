import json
from django.http        import JsonResponse
from django.views       import View
from .models            import FilteringColor, Product, SubCategory, Series, Sex, Color, ProductSize, Size, Medium, ProductInformation 

class DetailView(View):
    def get(self, request, serialNumber):
        product = Product.objects.get(serial_number=serialNumber)
        
        information_dict = {}

        information_dict['sub_category']        = product.sub_category.name
        information_dict['series_name']         = product.series.name
        information_dict['price']               = product.price
        information_dict['discount_rate']       = product.discount_rate
        information_dict['promotion']           = product.promotion.name
        information_dict['sex']                 = product.sex.name
        information_dict['simple_description']  = product.simple_description
        information_dict['color']               = product.color.name
        information_dict['serial_number']       = serialNumber
        information_dict['main_image']          = product.main_image
                
        sub_images = [i.medium_url for i in Medium.objects.filter(product=product.id)]
        information_dict['sub_images']          = sub_images

        information_dict['detail_description']  = product.series.detail_description
        information_dict['features']            = product.series.feature
        information_dict['series_sub_image']    = product.series.additional_image 
        information_dict['series_image']        = product.series.image 

        product_information                     = ProductInformation.objects.get(product_id=product.id)
        information_dict['material']            = product_information.material
        information_dict['manufacturer']        = product_information.manufacturer
        information_dict['country']             = product_information.country
        information_dict['caution']             = product_information.caution
        information_dict['assurance']           = product_information.quality_assurance
        information_dict['as_center']           = product_information.as_center
        information_dict['manufacture_date']    = product_information.manufacture_date

        size_list = []
        size_ids = ProductSize.objects.filter(product_id = product.id)
        for size_id in size_ids:
            size = size_id.size.name
            size_list.append(size)
        
        size_list.sort()
        information_dict['size_range']        = str(size_list[0])+' - '+str(size_list[-1])
        information_dict['size_list']         = size_list
        
        return JsonResponse({'product_information': [information_dict]}, status=200)