from django.db      import models
from false_account.models import Account
from product.models import Product, Size

class Cart(Models.model):
    account         = models.ForeignKey(Account, models.on_delete=CASCADE)
    product         = models.ForeignKey(Product, models.on_delete=CASCADE)
    size            = models.ForeignKey(Size, models.on_delete=CASCADE)
    quantity        = models.IntegerField(default=1)
    buy_now         = models.BooleanField(default=False)
    
    class Meta:
        db_table = "carts"
    
