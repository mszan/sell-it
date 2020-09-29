# -*- coding: utf-8 -*-
import os
from django.db import models
from django.contrib.auth.models import User

# Makes user's email field unique.
User._meta.get_field('email')._unique = True


def offer_image_upload_path(instance, filename):
    """
    Function that returns offer image upload path.
    :return: /images/users/{offer.id}/{filename}
    """
    ext = filename.split('.')[-1]
    filename = f'profile_picture.{ext}'
    return os.path.join('images', 'users', str(instance.user.id), filename)


class UserProfile(models.Model):
    """
    User profile model. Related with user auth model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_online = models.BooleanField(default=0)
    voivodeships = [(1, 'wielkopolskie'), (2, 'kujawsko-pomorskie'), (3, 'małopolskie'), (4, 'łódzkie'),
                    (5, 'dolnośląskie'), (6, 'lubelskie'), (7, 'lubuskie'), (8, 'mazowieckie'), (9, 'opolskie'),
                    (10, 'podlaskie'), (11, 'śląskie'), (12, 'podkarpackie'), (13, 'świętokrzyskie'),
                    (14, 'warmińsko-mazurskie'), (15, 'zachodniopomorskie')]
    voivodeship = models.IntegerField(choices=voivodeships, null=True)
    phone_number = models.PositiveIntegerField(null=True)
    phone_number_visible = models.BooleanField(default=0)   # Defines if phone number is visible to others on user's offers.
    profile_picture = models.ImageField(default='images/users/no_image.png',
                                        upload_to=offer_image_upload_path)

    def __str__(self):
        return f'{self.user} - profile'
