from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product, Combo
from .serializers import CategorySerializer, ProductSerializer, ComboSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer

    # GET /api/categories/active/
    @action(detail=False, methods=['get'])
    def active(self, request):
        active = Category.objects.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset         = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        available = self.request.query_params.get('available')

        if category:
            queryset = queryset.filter(category_id=category)
        if available:
            queryset = queryset.filter(is_available=True, is_active=True)
        return queryset

    # GET /api/products/available/
    @action(detail=False, methods=['get'])
    def available(self, request):
        products = Product.objects.filter(is_active=True, is_available=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ComboViewSet(viewsets.ModelViewSet):
    queryset         = Combo.objects.prefetch_related('products').all()
    serializer_class = ComboSerializer

    # GET /api/combos/active/
    @action(detail=False, methods=['get'])
    def active(self, request):
        active = Combo.objects.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)