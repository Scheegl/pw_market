from django.urls import path
from .views import LotsList, LotsDetail, create_lots, LotsCreate, LotsUpdate, LotsDelete


urlpatterns = [
    path('', LotsList.as_view()),
    path('<int:pk>', LotsDetail.as_view()),
    path('create/', LotsCreate.as_view(), name= 'create_lots'),
    path('<int:pk>/update/', LotsUpdate.as_view(), name='lots_update'),
    path('<int:pk>/delete/', LotsDelete.as_view(), name='product_delete'),
]