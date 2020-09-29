# -*- coding: utf-8 -*-
from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from rest_framework import viewsets, permissions

from messages.forms import MessageSendForm
from messages.models import Conversation
from offers.models import Category, Offer, OfferImage, User
from .forms import OfferAddForm, OfferImageAddForm, OfferDeleteForm, OfferEditForm, OfferSearchForm
from .serializers import CategorySerializer, OfferSerializer, OfferImageSerializer


def get_offer_images_urls(offer_id):
    """
    Function that returns dicionary of offer images related to given offer.
    If no images are found, it returns dictionary with default image.
    :param offer_id: Offer ID.
    """
    result = []
    objs = OfferImage.objects.filter(offer_id=offer_id).exclude(index=0)
    if objs:
        for obj in objs:
            result.append(getattr(obj, 'image'))
    else:
        result = [OfferImage._meta.get_field('image').get_default()]
    return result


def get_offer_thumbnail(offer_id):
    """
    Function that returns offer thumbnail.
    If no thumbnail is found, it returns field default value.
    :param offer_id: Offer ID.
    """
    thumbnail = OfferImage.objects.filter(offer_id=offer_id, index=0).first()
    if thumbnail:
        return thumbnail.image
    else:
        return OfferImage._meta.get_field('image').get_default()


class HomeView(TemplateView):
    """
    "Home" page view.
    """
    template_name = 'offers/home.html'

    def get_context_data(self, **kwargs):
        # Return dictionary of 6 recently added offers.
        recent_offers_all = Offer.objects.filter(status=1).order_by('-date_added')
        recent_offers = recent_offers_all[:6]
        count = 0
        recent_offers_list = []
        for offer in recent_offers:
            if count >= 5:
                break
            temp = {'images': (get_offer_images_urls(offer))}
            if temp['images'][0] != 'images/offers/no_image.png':
                temp['id'] = getattr(offer, 'id')
                temp['title'] = getattr(offer, 'title')
                temp['price'] = getattr(offer, 'price')
                temp['description'] = getattr(offer, 'description')
                recent_offers_list.append(temp)
                count += 1

        context = {'page_title': 'Home', 'recent_offers': recent_offers_list, }
        return context


class AboutView(TemplateView):
    """
    "About" page view.
    """
    template_name = 'offers/about.html'

    def get_context_data(self, **kwargs):
        context = {'page_title': 'About', 'categories': Category.objects.filter(status=1), }
        return context


def get_category(url):
    """
    Function that returns category with specific url or returns None.
    :param url: Category url.
    """
    try:
        cat = Category.objects.get(url=url)
    except Category.DoesNotExist:
        return None
    else:
        return cat


class CategoryView(ListView):
    """
    Specific offers' category view.
    """
    model = Offer
    template_name = 'offers/category.html'
    context_object_name = 'offers'
    ordering = ['id']
    paginate_by = 10

    def get_queryset(self, **kwargs):
        category = get_category(url=self.kwargs.get('name'))
        if category:
            if category.is_leaf_node():
                offers = Offer.objects.filter(category=category, status=1).values()
            else:
                offers = Offer.objects.none()
                subcategories = category.get_descendants()
                for subcategory in subcategories:
                    offers |= Offer.objects.filter(category=subcategory, status=1)
                offers = offers.order_by('-id').values()
            for offer in offers:
                offer['thumbnail'] = get_offer_thumbnail(offer['id'])
                offer['owner'] = User.objects.get(id=offer['owner_id'])
        else:
            offers = None
        return offers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = get_category(url=self.kwargs.get('name'))
        return context


def get_owner_random_offers(offer):
    """
    Function that returns dictionary of 3 random offer owner's offers.
    :param offer: Offer object.
    """
    offers = Offer.objects.filter(owner=offer['owner']).order_by('?').exclude(id=offer['id'])[:3]
    result = []
    for offer in offers:
        temp = {'id': getattr(offer, 'id'), 'title': getattr(offer, 'title'),
                'description': getattr(offer, 'description'), 'thumbnail': get_offer_thumbnail(offer.id), }
        result.append(temp)
    return result


class OfferView(DetailView):
    """
    Offer details view.
    Handles GET request to show actual offer details.
    Handles POST request to create related Conversation and Message object.
    """
    model = Offer
    template_name = 'offers/offer_details.html'

    def post(self, request, *args, **kwargs):
        message_send_form = MessageSendForm(self.request.POST)
        if message_send_form.is_valid():
            offer = get_object_or_404(Offer, id=self.kwargs.get('pk'))
            conversation = Conversation(interlocutor_1=self.request.user, interlocutor_2=offer.owner, offer=offer)
            conversation.save()

            message = message_send_form.save(commit=False)
            message.owner = self.request.user
            message.conversation = conversation
            message.save()

            messages.success(self.request, 'Message has been sent successfully.')
            return redirect('conversation', pk=message.conversation.id)
        messages.info(self.request, 'Message could not be sent.')

    def get_context_data(self, **kwargs):
        """
        Function that tries to obtain specified offer object or returns 404.
        """
        try:
            offer = get_object_or_404(Offer, id=self.kwargs.get('pk')).__dict__
            offer['condition'] = Offer.objects.get(id=offer['id']).get_condition_display()
            offer['category'] = Category.objects.get(id=offer['category_id'])
            offer['owner'] = User.objects.get(id=offer['owner_id'])
            offer['images'] = get_offer_images_urls(offer['id'])
        finally:
            pass

        context = {'page_title': offer['title'], 'random_user_offers': get_owner_random_offers(offer),
                   'offer': offer, 'message_send_form': MessageSendForm(), }
        return context


class OfferAddView(LoginRequiredMixin, TemplateView):
    """
    Offer add view that handles adding new offers.
    """
    model = Offer
    template_name = 'offers/offer_add_form.html'

    def get(self, request, *args, **kwargs):
        offer_add_form = OfferAddForm()
        context = {'offer_add_form': offer_add_form, 'offer_image_add_forms': []}

        # Appends to context offer image forms.
        for i in range(0, 5):
            context['offer_image_add_forms'].append(OfferImageAddForm(prefix=f'offer_image_add_form_{i + 1}'))

        return render(request, 'offers/offer_add_form.html', context)

    def post(self, request, *args, **kwargs):
        owner = request.user
        request_cp = request.POST.copy()
        request_cp['category'] = Category.objects.get(name=request_cp['category'])

        offer_add_form = OfferAddForm(request_cp)

        if offer_add_form.is_valid():
            obj = Category.objects.get(name=offer_add_form.data['category'])
            offer = offer_add_form.save(commit=False)
            offer.category_id = getattr(obj, 'id')
            offer.owner = owner
            offer.save()

            for i in range(0, 5):
                offer_image_add_form = OfferImageAddForm(request.POST, request.FILES,
                                                         prefix=f'offer_image_add_form_{i + 1}')
                if offer_image_add_form.is_valid() and offer_image_add_form.cleaned_data['image'] != 'images/offers/no_image.png':
                    offer_image = offer_image_add_form.save(commit=False)
                    offer_image.offer_id = offer.id
                    offer_image.index = i + 1
                    offer_image.save()

            messages.success(request, 'Offer added successfully.')
        else:
            messages.warning(request, 'Unable to add offer.')
        return redirect('offer', pk=offer_add_form.instance.id)


class OfferEditView(LoginRequiredMixin, TemplateView):
    """
    Offer edit view. Used to edit offers that are already posted.
    """
    model = Offer
    template_name = 'offers/offer_add_form.html'

    def get(self, request, *args, **kwargs):
        offer_instance = Offer.objects.get(id=self.kwargs.get('pk'))

        # Check if user is offer's owner. If not, redirect to offer details page.
        if request.user != offer_instance.owner:
            messages.warning(request, 'You are not allowed to edit this offer.')
            return redirect('offer', pk=offer_instance.id)
        offer_edit_form = OfferEditForm(instance=offer_instance)
        context = {'offer_edit_form': offer_edit_form, 'offer_image_edit_forms': []}

        for i in range(0, 5):
            try:
                offer_image_instance = OfferImage.objects.get(offer=offer_instance, index=i + 1)
            except OfferImage.DoesNotExist:
                offer_image_instance = None

            offer_image_edit_form = OfferImageAddForm(prefix=f'offer_image_add_form_{i + 1}',
                                                      instance=offer_image_instance)
            context['offer_image_edit_forms'].append(offer_image_edit_form)

        return render(request, 'offers/offer_edit_form.html', context)

    def post(self, request, *args, **kwargs):
        offer_instance = Offer.objects.get(id=self.kwargs.get('pk'))

        # Check if user is offer's owner. If not, redirect to offer details page.
        if request.user != offer_instance.owner:
            messages.warning(request, 'You are not allowed to edit this offer.')
            return redirect('offers-home')

        request_cp = request.POST.copy()
        request_cp['category'] = Category.objects.get(name=request_cp['category'])
        offer_edit_form = OfferEditForm(request_cp, instance=offer_instance)

        if offer_edit_form.is_valid():
            obj = Category.objects.get(name=offer_edit_form.data['category'])
            offer = offer_edit_form.save(commit=False)
            offer.category_id = getattr(obj, 'id')
            offer.save()

            for i in range(0, 5):
                try:
                    offer_image_instance = OfferImage.objects.get(offer=offer_instance, index=i + 1)
                except OfferImage.DoesNotExist:
                    offer_image_instance = None

                offer_image_add_form = OfferImageAddForm(request.POST, request.FILES,
                                                         prefix=f'offer_image_add_form_{i + 1}',
                                                         instance=offer_image_instance)

                if offer_image_add_form.is_valid() and offer_image_add_form.cleaned_data['image'] != 'images/offers/no_image.png':
                    offer_image = offer_image_add_form.save(commit=False)
                    offer_image.offer_id = offer.id
                    offer_image.index = i + 1
                    offer_image.save()

            messages.success(request, 'Offer updated successfully.')
        else:
            messages.warning(request, 'Unable to add offer.')
        return redirect('offer', pk=offer_instance.id)


class OfferDeleteView(LoginRequiredMixin, TemplateView):
    """
    Offer delete view. It does not delete object itself but it sets its status to inactive.
    """
    def get(self, request, *args, **kwargs):
        offer_delete_form = OfferDeleteForm()
        context = {'offer_delete_form': offer_delete_form, }
        return render(request, 'offers/offer_delete_form.html', context)

    def post(self, request, *args, **kwargs):
        offer_delete_form = OfferDeleteForm(request)
        offer = Offer.objects.get(id=self.kwargs.get('pk'))
        if offer_delete_form.is_valid() and request.user == offer.owner:
            offer.status = 0
            offer.save()
            messages.success(request, 'Offer deleted.')
        else:
            messages.warning(request, 'Something went wrong. We were unable to delete the offer.')
        return redirect('user-details', pk=offer.owner.id)


class OfferImagesDeleteAllView(LoginRequiredMixin, TemplateView):
    """
    View that handles deleting all of image objects.
    TODO: Remove files in storage too.
    """
    template_name = 'offers/base.html'

    def post(self, request, *args, **kwargs):
        offer_instance = Offer.objects.get(id=self.kwargs.get('pk'))
        if request.user != offer_instance.owner:
            messages.warning(request, 'You are not allowed to remove images from this offer.')
            return redirect('offer', pk=offer_instance.id)
        offer_images = OfferImage.objects.filter(offer=offer_instance)
        offer_images.delete()
        messages.success(request, 'Photos deleted.')
        return redirect('offer-edit', pk=offer_instance.id)


class OfferSearchView(ListView):
    """
    Offer search view. Used to get search results and display them.
    """
    model = Offer
    template_name = 'offers/offer_search_results.html'
    context_object_name = 'offers'
    ordering = ['id']
    paginate_by = 10

    def post(self, request, *args, **kwargs):
        search_form = OfferSearchForm(request.POST)
        if search_form.is_valid():
            search_query = search_form.cleaned_data['title']
        else:
            messages.info(request, 'Wrong search query.')
            return redirect('Home')

        base_url = reverse('offer-search')
        query_string = urlencode({'query': search_query})
        search_url = '{}?{}'.format(base_url, query_string)
        return redirect(search_url)

    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get('query')

        if 2 < len(search_query) < 40:
            # offers = Offer.objects.filter(title__contains=search_query).values()
            offers = Offer.objects.annotate(search=SearchVector('title', 'description', 'owner__username'), ).filter(
                search=search_query).values()
        else:
            offers = Offer.objects.none()

        for offer in offers:
            offer['thumbnail'] = get_offer_thumbnail(offer['id'])
            offer['owner'] = User.objects.get(id=offer['owner_id'])
        return offers

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('query')
        context['page_title'] = 'Search results'
        return context


# API Views.


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class OfferImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = OfferImage.objects.all()
    serializer_class = OfferImageSerializer
    permission_classes = [permissions.IsAuthenticated]
