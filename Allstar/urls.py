from django.urls import path

urlpatterns = [
    path('/account', include('account.urls')),
    path('/products', include('product.urls')),
]