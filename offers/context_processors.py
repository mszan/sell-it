from random import randint
from .models import Category, Offer
from .forms import OfferSearchForm


def get_all_categories(request):
    """
    Function that returns active category objects.
    """
    return {'categories': Category.objects.filter(status=1)}


def get_offer_search_form(request):
    """
    Function that returns offer search form.
    """
    return {'offer_search_form': OfferSearchForm()}


def get_random_offer_id(request):
    """
    Function that returns random offer's primary key.
    """
    offers_active = Offer.objects.filter(status=1)
    context = {}
    if len(offers_active) == 0:
        # If there are no offers, return "1" to avoid errors.
        context['get_random_offer_id'] = 1
    else:
        # If there are any offers, return random and get its primary key.
        context['get_random_offer_id'] = Offer.objects.filter(status=1)[randint(0, len(offers_active) - 1)].id
    return context
