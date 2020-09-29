from django.contrib import admin
from offers.models import Category, Offer, OfferImage
from mptt.admin import MPTTModelAdmin

# Register as MPTT.
admin.site.register(Category, MPTTModelAdmin)

# Register as normal model.
admin.site.register(Offer)
admin.site.register(OfferImage)
