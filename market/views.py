from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from APIMain.models import Product
from APIMain.serializers import ProductSerializer



# Create your views here.

def MarketView(request):
    return render(request, "marketPage.html")

class FilterPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 4
    


class ProductFilterView(APIView):
    
    pagination_class = FilterPagination
    
    
    def get(self, request):
        
        paginator = self.pagination_class()
        
        #search = request.data["search"]
        search = request.GET.get("search", "").strip()

        if not search:
            print('Entro porque no search')
            return Response({"message": "Por favor, ingrese un término de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)
        
        query_set = Product.objects.filter(
            Q(name__icontains = search) |
            Q(category__icontains = search) |
            Q(description__icontains = search)
        )
        
        if not query_set.exists():
            print('Entro porque no existe')
            return Response({"message": f"Valor no encontrado para {search}"}, status=status.HTTP_404_NOT_FOUND)
        
        paginator_products = paginator.paginate_queryset(query_set, request, view=self)
        serializer = ProductSerializer(paginator_products, many=True)
        
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)


def product_filter_view(request):
    return render(request, 'search_products.html')