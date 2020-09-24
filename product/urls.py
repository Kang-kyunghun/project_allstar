from django.urls        import path
from .views             import ProductView, MainView, ListView, SearchView

urlpatterns = [
    path('/<int:id>', ProductView.as_view()),
    path('/main', MainView.as_view()),
    path('', ListView.as_view()),
    path('/search', SearchView.as_view()),
]