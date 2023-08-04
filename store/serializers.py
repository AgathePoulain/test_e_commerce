from rest_framework.serializers import ModelSerializer
from store.models import Product


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product  # Specify the model we try to serialize
        fields = '__all__'  # Specify the fields from this model which will be included in the process : here we want
        # to work with all the fields of the Post model
