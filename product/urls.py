from django.urls        import path
from .views             import ProductView

urlpatterns = [
    path('/<int:id>', ProductView.as_view()),
]