from django.urls import path
from .views import LoginPageView, ProductListView, CreateProductView, ViewProducts,LogoutView

urlpatterns = [
    path('login/', LoginPageView.as_view(), name="login"),
    path('Probes/', CreateProductView.as_view(), name='Probes'),
    path('products/', ViewProducts, name='products'),
    path('logout/', LogoutView, name='logout'),
    path('list-products/', ProductListView.as_view(), name='list-products'),
    
]