from django.db      import models
from false_account.models import Account
from product.models import Product, Size

class Cart(Models.model):
    account         = models.ForeignKey(Account, on_delete=models.CASCADE)
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    size            = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity        = models.IntegerField(default=1)
    buy_now         = models.BooleanField(default=False)
    
    class Meta:
        db_table = "carts"
    
