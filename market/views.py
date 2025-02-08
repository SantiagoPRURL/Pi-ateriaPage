from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from APIMain.models import Product



# Create your views here.

def MarketView(request):
    return render(request, "marketPage.html")


class ProductFilterView(APIView):
    def get(self, request):
        return Response({"message":"Hi"})
