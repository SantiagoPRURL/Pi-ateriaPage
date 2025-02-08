from django.shortcuts import render

# Create your views here.

def MarketView(request):
    return render(request, "marketPage.html")
