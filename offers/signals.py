from django.core.files.storage import default_storage
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import OfferImage
from PIL import Image
from django.conf import settings
import requests
from io import BytesIO


@receiver(pre_save, sender=OfferImage)
def delete_old_thumbnail(sender, instance, **kwargs):
    # TODO: Update -> Create thumbnail from FIRST FOUND photo in offer.
    """
    Deletes old instance of thumbnail if it exists.
    :param sender: Offer image model.
    """
    if instance.index == 1:
        try:
            OfferImage.objects.filter(index=0, offer=instance.offer).delete()
        except OfferImage.DoesNotExist:
            pass


@receiver(post_save, sender=OfferImage)
def create_thumbnail(sender, instance, created, **kwargs):
    """
    Creates a new instance of thumbnail based on first image.
    :param sender: Offer image model
    """
    if instance.index == 1:
        # Try to get first image.
        try:
            img_instance = OfferImage.objects.get(index=instance.index, offer=instance.offer)
        # If first image is not found, do not create thumbnail.
        except OfferImage.DoesNotExist:
            pass
        else:
            # If first image is found, create thumbnail.
            img = Image.open(img_instance.image)
            img_instance.image.name = img_instance.image.name.replace(f'image_1', 'image_0')

            img.thumbnail((400, 250))
            # img = img.convert("RGB")
            # f"{settings.MEDIA_URL}{img_instance.image.name}"
            print("DDDDD", img_instance.image.path)
            img.save(img_instance.image.path)

            OfferImage.objects.create(index=0, offer=instance.offer, image=img_instance.image)
