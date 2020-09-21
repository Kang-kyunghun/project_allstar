from django.urls import path, include

from .views      import MainListView, Chuck70ListView

urlpatterns = [
    path('/shose', MainListView.as_view()),
    path('/chuck70', Chuck70ListView.as_view()),
]
