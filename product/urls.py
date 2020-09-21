from django.urls        import path
from .views             import DetailView

urlpatterns = [
    path('/<str:serialNumber>', DetailView.as_view()),
]