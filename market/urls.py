from django.urls import path
from .views import MarketView


urlpatterns = [
    path('market/', MarketView, name="mainPage"),
]