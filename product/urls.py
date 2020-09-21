from django.urls import path, include

from .views import MainListView, SubCategotyListView

urlpatterns = [
    path('/shose', MainListView.as_view()),
    path('/<str:sub>', SubCategotyListView.as_view()),
]
