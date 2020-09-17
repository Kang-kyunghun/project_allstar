from django.db              import models

class Category(models.Model):
    category                = models.CharField(max_length = 50)
  
    def __str__(self):
        return self.category 
    
    class Meta:
        db_table            = 'categories'

class SubCategory(models.Model):
    sub_category            = models.CharField(max_length = 50)
  
    def __str__(self):
        return self.sub_category 
    
    class Meta:
        db_table            = 'sub_categories'

class Series(models.Model):
    name                    = models.CharField(max_length = 100)
    detail_description      = models.TextField()
    feature                 = models.URLField()
    additional_image        = models.URLField()
    image                   = models.URLField()

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table            = 'serieses'

class Sex(models.Model):
    sex                     = models.CharField(max_length = 50)

    def __str__(self):
        return self.sex 
    
    class Meta:
        db_table            = 'sexes'

class FilteringColor(models.Model):
    filtering_color         = models.CharField(max_length = 100)

    def __str__(self):
        return self.filtering_color 
    
    class Meta:
        db_table            = 'filtering_colors'

class Color(models.Model):
    color                   = models.CharField(max_length = 100)
    filtering_color         = models.ForeignKey(FilteringColor, on_delete = models.CASCADE) 

    def __str__(self):
        return self.color 
    
    class Meta:
        db_table            = 'colors'

class Promotion(models.Model):
    promotion               = models.CharField(max_length = 50, null = True)
    
    def __str__(self):
        return self.promotion 
    
    class Meta:
        db_table            = 'promotions'

class Silouette(models.Model):
    silouette               = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.silouette 
    
    class Meta:
        db_table            = 'silouettes'

class Size(models.Model):
    size                    = models.IntegerField(default = 0)

    def __str__(self):
        return self.size 
    
    class Meta:
        db_table            = 'sizes'

class Product(models.Model):
    serial_number           = models.CharField(max_length = 50)
    category                = models.ForeignKey(Category, on_delete = models.CASCADE)
    sub_category            = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    serise                  = models.ForeignKey(Series, on_delete = models.CASCADE)
    main_image              = models.URLField()
    hover_image             = models.URLField()
    price                   = models.IntegerField(default = 0)
    discount_rate           = models.IntegerField(default = 0)
    sex                     = models.ForeignKey(Sex, on_delete = models.CASCADE)
    simple_description      = models.CharField(max_length = 200)
    color                   = models.ForeignKey(Color, on_delete = models.CASCADE)
    size                    = models.ManyToManyField(Size) 
    promotion               = models.ForeignKey(Promotion, on_delete = models.CASCADE)
    silouette               = models.ForeignKey(Silouette, on_delete = models.CASCADE)
    score                   = models.DecimalField(max_digits = 5, decimal_places = 2)
    created_at              = models.DateTimeField(auto_now_add = True)
    updated_at              = models.DateTimeField(auto_now = True) 

    def __str__(self):
        return self.serial_number 
    
    class Meta:
        db_table            = 'products'

class Medium(models.Model):
    product                 = models.ForeignKey(Product, on_delete = models.CASCADE)
    medium_url              = models.URLField()
    medium_type             = models.CharField(max_length = 100)
    
    class Meta:
        db_table            = 'media'

class ProductInformation(models.Model):
    product                 = models.ForeignKey(Product, on_delete = models.CASCADE)
    material                = models.CharField(max_length = 100) 
    minimum_size            = models.IntegerField(default = 0)
    maximum_size            = models.IntegerField(default = 0)
    manufacture             = models.CharField(max_length = 100)
    country                 = models.CharField(max_length = 100)
    caution                 = models.CharField(max_length = 200)
    quality_assureance      = models.CharField(max_length = 100)
    as_center               = models.CharField(max_length = 100)
    manufacture_date        = models.CharField(max_length = 100)
    
    class Meta:
        db_table            = 'product_informations'

