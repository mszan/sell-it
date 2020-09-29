from .models import Category, Offer, OfferImage
from users.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'status', 'name', 'url', 'desc', 'thumbnail', 'parent']


class OfferImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OfferImage
        fields = ['id', 'image', 'index', 'offer']


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ['id', 'status', 'category', 'owner', 'title', 'price', 'condition', 'description', 'date_added', 'offer_images']
        depth = 1