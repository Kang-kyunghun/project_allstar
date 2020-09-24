from django.db      import models

from product.models import Product 

class Account(models.Model):
    email               = models.CharField(max_length=100, unique = True)
    name                = models.CharField(max_length=30)
    sex                 = models.CharField(max_length=30)
    phone_number        = models.CharField(max_length=15, unique = True)
    date_of_birth       = models.DateTimeField(auto_now=False, auto_now_add=False) 
    password            = models.CharField(max_length=300) 
    is_agreed_emailing  = models.BooleanField(default=False) 
    is_agreed_texting   = models.BooleanField(default=False)
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)
    wishlist            = models.ManyToMany(Product, through = 'Wishlist')

    def __str__(self):
        return self.email

    class Meta:
        db_table = "accounts"

class Wishlist(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlists'