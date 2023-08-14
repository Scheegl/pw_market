from django.urls import path
from .views import LotsList, LotsDetail


urlpatterns = [
    path('', LotsList.as_view()),
    path('<int:pk>', LotsDetail.as_view()),
]