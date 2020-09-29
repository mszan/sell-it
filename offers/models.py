# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
import os


def offer_image_upload_path(instance, filename):
    """
    Function that returns offer image upload path.
    :return: /images/offers/{offer.id}/{filename}
    """
    ext = filename.split('.')[-1]
    filename = f'image_{instance.index}.{ext}'
    return os.path.join('images', 'offers', str(instance.offer.id), filename)


class Category(MPTTModel):
    """
    Category model. Used by Offer object.
    """
    status_choices = [(1, 'Active'),
                      (2, 'Not active')]
    status = models.IntegerField(choices=status_choices)
    name = models.CharField(max_length=25)
    url = models.CharField(max_length=25)
    desc = models.CharField(max_length=400, blank=True)     # Description. Used by root categories that are shown on home page.
    thumbnail = models.ImageField(upload_to='images/offers/categories',
                                  default='images/offers/no_image.png')   # Used by root categories that are shown on home page.
    parent = TreeForeignKey('self', blank=True, null=True, related_name='child', db_index=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Offer(models.Model):
    """
    Offer model.
    """
    status_choices = [(1, 'Active'),
                      (2, 'Not active')]
    status = models.IntegerField(choices=status_choices, default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    condition_choices = [(1, 'Brand new'),
                      (2, 'Renewed'),
                      (3, 'Used - very good'),
                      (4, 'Used - good'),
                      (5, 'Used - acceptable')]
    condition = models.IntegerField(choices=condition_choices)
    description = models.CharField(max_length=2000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Offer ID: {self.id}. Title: {self.title}.'


class OfferImage(models.Model):
    """
    Offer image model.
    """
    offer = models.ForeignKey(Offer, related_name='offer_images', on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to=offer_image_upload_path,
                              default='images/offers/no_image.png')
    # Field that is used to determinate offer images order and thumbnail. 0 - thumbnail, 1 - main image, 2-5 - the rest.
    index = models.IntegerField(default=1)

    class Meta:
        verbose_name_plural = 'Offer Images'

    def __str__(self):
        return f'Offer ID: {self.offer_id}. Name: {self.image.name}.'
