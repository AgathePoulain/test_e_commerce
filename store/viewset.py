from store.models import Product
from store.serializers import ProductSerializer
from rest_framework import viewsets


class ProductViewset(viewsets.ModelViewSet):
    """
    Get --> List --> QuerySet
    Get --> Retrieve
    Post --> Create
    Put --> Update
    Patch --> Partial Update
    Delete --> Destroy
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
