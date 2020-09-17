from django.db   import models

class Category(models.Model):
    name = models.CharField(max_length = 50)
  
    def __str__(self):
        return self.category 
    
    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name     = models.CharField(max_length = 50)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table  = 'sub_categories'

class Series(models.Model):
    name                = models.CharField(max_length = 100)
    detail_description  = models.TextField()
    feature             = models.URLField()
    additional_image    = models.URLField(null = True)
    image               = models.URLField()

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'series'

class Sex(models.Model):
    name = models.CharField(max_length = 50)

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'sexes'

class FilteringColor(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'filtering_colors'

class Color(models.Model):
    name            = models.CharField(max_length = 100)
    filtering_color = models.ForeignKey(FilteringColor, on_delete = models.CASCADE) 

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'colors'

class Promotion(models.Model):
    name = models.CharField(max_length = 50, null = True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'promotions'

class Silouette(models.Model):
    name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'silouettes'

class Size(models.Model):
    name = models.IntegerField(default = 0)

    def __str__(self):
        return self.name 
    
    class Meta:
        db_table = 'sizes'

class Product(models.Model):
    serial_number       = models.CharField(max_length = 50)
    category            = models.ForeignKey(Category, on_delete = models.CASCADE)
    sub_category        = models.ForeignKey(SubCategory, on_delete = models.CASCADE)
    series              = models.ForeignKey(Series, on_delete = models.CASCADE)
    main_image          = models.URLField()
    hover_image         = models.URLField()
    price               = models.DecimalField(max_digits = 10, decimal_places = 4)
    discount_rate       = models.DecimalField(max_digits = 3, decimal_places = 2, null = True)
    sex                 = models.ForeignKey(Sex, on_delete = models.CASCADE)
    simple_description  = models.CharField(max_length = 200, null = True)
    color               = models.ForeignKey(Color, on_delete = models.CASCADE)
    size                = models.ManyToManyField(Size, through = 'ProductSize') 
    promotion           = models.ForeignKey(Promotion, on_delete = models.CASCADE, null = True)
    silouette           = models.ForeignKey(Silouette, on_delete = models.CASCADE, null = True)
    score               = models.DecimalField(max_digits = 5, decimal_places = 2)
    created_at          = models.DateTimeField(auto_now_add = True)
    updated_at          = models.DateTimeField(auto_now = True) 

    def __str__(self):
        return self.serial_number 
    
    class Meta:
        db_table = 'products'

class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    size    = models.ForeignKey(Size, on_delete = models.CASCADE)
    
    class Meta:
        db_table = 'products_sizes'

class Medium(models.Model):
    product     = models.ForeignKey(Product, on_delete = models.CASCADE)
    medium_url  = models.URLField()
    medium_type = models.CharField(max_length = 100)
    
    class Meta:
        db_table = 'media'

class ProductInformation(models.Model):
    product           = models.ForeignKey(Product, on_delete = models.CASCADE)
    material          = models.CharField(max_length = 100) 
    minimum_size      = models.IntegerField(default = 0)
    maximum_size      = models.IntegerField(default = 0)
    manufacturer      = models.CharField(max_length = 100)
    country           = models.CharField(max_length = 100)
    caution           = models.CharField(max_length = 200)
    quality_assurance = models.CharField(max_length = 100)
    as_center         = models.CharField(max_length = 100)
    manufacture_date  = models.CharField(max_length = 100)
    
    class Meta:
        db_table = 'product_informations'

