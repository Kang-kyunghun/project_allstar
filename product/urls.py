from django.urls import path, include

from .views import ListView, MainView

urlpatterns = [
    path('/main', MainView.as_view()),
    path('', ListView.as_view()),
]