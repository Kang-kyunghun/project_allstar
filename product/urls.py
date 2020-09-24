from django.urls        import path
<<<<<<< HEAD
from .views             import ProductView, ListView, MainView
=======
from .views             import ProductView, MainView, ListView
>>>>>>> master

urlpatterns = [
    path('/<int:id>', ProductView.as_view()),
    path('/main', MainView.as_view()),
    path('', ListView.as_view()),
]