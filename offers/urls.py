from django.urls import path
from offers.views import HomeView, AboutView, CategoryView, OfferView, OfferAddView, OfferDeleteView, OfferEditView, \
    OfferSearchView, OfferImagesDeleteAllView
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    path('favicon.ico',
         RedirectView.as_view(
             url=staticfiles_storage.url('img/favicon.ico')
         )),

    path('offers/',
         HomeView.as_view(),
         name='offers-home'),

    path('offer/<int:pk>/',
         OfferView.as_view(),
         name='offer'),

    path('offer/<int:pk>/delete/',
         OfferDeleteView.as_view(),
         name='offer-delete'),

    path('offer/<int:pk>/edit/',
         OfferEditView.as_view(),
         name='offer-edit'),

    path('offer/<int:pk>/edit/delete-images-all/',
         OfferImagesDeleteAllView.as_view(),
         name='offer-edit-delete-images-all'),

    path('offer/search/',
         OfferSearchView.as_view(),
         name='offer-search'),

    path('offer/add/',
         OfferAddView.as_view(),
         name='offer-add'),

    path('category/<str:name>/',
         CategoryView.as_view(),
         name='offers-category'),

    path('about/',
         AboutView.as_view(),
         name='offers-about'),

    path('home/',
         HomeView.as_view(),
         name='offers-home'),

    path('',
         HomeView.as_view(),
         name='offers-home'),
]