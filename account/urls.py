from django.urls        import path
from .views             import SignInView, SignUpView, WishlistView

urlpatterns = [
        path('/signup', SignUpView.as_view()), 
        path('/signin', SignInView.as_view()), 
        path('/wishlist', WishlistView.as_view()), 
]