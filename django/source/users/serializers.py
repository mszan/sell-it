from .models import User, UserProfile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """
    User seralizer. Used to obtain basic user fields.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    """
    User profile seralizer. Used to obtain basic user profile's fields.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'is_online', 'voivodeship', 'profile_picture', 'phone_number_visible']
        depth = 1
