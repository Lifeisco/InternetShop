from rest_framework.serializers import ModelSerializer

from main.models import ItemsInStorage


class StorageSerializer(ModelSerializer):
    class Meta:
        model = ItemsInStorage
        fields = ['item', 'storage', 'stock']
