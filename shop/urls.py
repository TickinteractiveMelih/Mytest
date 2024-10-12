from django.urls import path

from django.shortcuts import render


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from shop import views



urlpatterns = [
    path('my-products/', views.UserProductsView.as_view(), name='user_products'),
    path('add-product/', views.AddProductView.as_view(), name='add_product'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

