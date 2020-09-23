from django.urls        import path
from .views             import ProductView, ListView, MainView

urlpatterns = [
    path('/<int:id>', ProductView.as_view()),
    path('/main', MainView.as_view()),
    path('', ListView.as_view()),
]