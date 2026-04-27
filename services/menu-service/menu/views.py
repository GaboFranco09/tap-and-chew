from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product, Combo
from .serializers import CategorySerializer, ProductSerializer, ComboSerializer
from .middleware import IsInternalRequest


class CategoryViewSet(viewsets.ModelViewSet):
    queryset            = Category.objects.all()
    serializer_class    = CategorySerializer
    permission_classes  = [IsInternalRequest]

    @action(detail=False, methods=['get'])
    def active(self, request):
        active     = Category.objects.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset            = Product.objects.select_related('category').all()
    serializer_class    = ProductSerializer
    permission_classes  = [IsInternalRequest]

    def get_queryset(self):
        queryset  = super().get_queryset()
        category  = self.request.query_params.get('category')
        available = self.request.query_params.get('available')
        if category:
            queryset = queryset.filter(category_id=category)
        if available:
            queryset = queryset.filter(is_available=True, is_active=True)
        return queryset

    @action(detail=False, methods=['get'])
    def available(self, request):
        products   = Product.objects.filter(is_active=True, is_available=True)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ComboViewSet(viewsets.ModelViewSet):
    queryset            = Combo.objects.prefetch_related('products').all()
    serializer_class    = ComboSerializer
    permission_classes  = [IsInternalRequest]

    @action(detail=False, methods=['get'])
    def active(self, request):
        active     = Combo.objects.filter(is_active=True)
        serializer = self.get_serializer(active, many=True)
        return Response(serializer.data)