from django.urls        import path
from .views             import DetailView

urlpatterns = [
    path('/<int:id>', DetailView.as_view()),
]