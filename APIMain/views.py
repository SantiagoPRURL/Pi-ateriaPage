from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from rest_framework.parsers import MultiPartParser, FormParser #Permite manejar archivos
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# Create your views here.
class LoginPageView(APIView):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        username = request.data.get("Username")
        password = request.data.get("Password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        
            return Response({"message":"Usuario Logeado con exito", "redirect":"/api/products/"}, status=status.HTTP_200_OK)
        return Response({"error":"Usuario No Logeado", "redirect":"/api/login/"}, status=status.HTTP_400_BAD_REQUEST)
        
class CreateProductView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
           return redirect("login")
        else:
            return render(request, "createProduct.html")  
   
    def post(self, request):
        self.parser_classes = (MultiPartParser, FormParser)
        serializer = ProductSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductPagination(PageNumberPagination):
    page_size = 4 
    page_size_query_param = 'page_size'  # Permite cambiar el tamaño en la URL
    max_page_size = 4  # Tamaño máximo permitido
    
    
class ProductListView(APIView):
    pagination_class = ProductPagination
    
    def get(self, request):
        products = Product.objects.all()
        paginator = self.pagination_class()
        paginated_products = paginator.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(paginated_products, many=True)
        return Response({
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
        
    def delete(self, request):     
        if not request.user.is_authenticated:
            return Response({"error": "No estás autenticado"}, status=status.HTTP_403_FORBIDDEN)
        
        name = request.data.get('name')
        
        if not name:
            return Response({"error": "El nombre es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(name = name)
            product.delete()
            return Response({'message':'Producto eliminado con exito'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'error':'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        

def ViewProducts(request):
    if not request.user.is_authenticated:
        return redirect("login")   
    else: 
        return render(request, "ViewProduct.html")
  
def LogoutView(request):
    logout(request)
    return Response({"message":"Usuario acaba de salir", "redirect":"/api/login/"}, status=status.HTTP_200_OK)
    
class ProductFilterView(APIView):
    def get(self, request):
        queryset = Product.objects.all()
    
        name = request.query_params.get('name', None)
        category = request.query_params.get('category')
        
        if name: 
            queryset.filter(name__icontains = name)
        if category:
            queryset.filter(category__icontains = category)
        
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
            
