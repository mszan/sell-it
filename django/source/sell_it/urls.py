"""sell_it URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from offers.views import CategoryViewSet, OfferViewSet, OfferImageViewSet
from users.views import UserProfileViewSet, UserViewSet
from messages.views import ConversationViewSet, MessageViewSet

# REST Framework routers.
router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('offers', OfferViewSet)
router.register('offers-images', OfferImageViewSet)
router.register('users', UserViewSet)
router.register('users-profiles', UserProfileViewSet)
router.register('conversations', ConversationViewSet)
router.register('messages', MessageViewSet)

urlpatterns = [
    # App urls.
    path('admin/', admin.site.urls),
    path('', include('offers.urls')),
    path('', include('users.urls')),
    path('', include('messages.urls')),

    # API urls.
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)