from django.urls import path

urlpatterns = [
    path('/account', include('account.urls')),
    path('/product', include('product.urls')),
]