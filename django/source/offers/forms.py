# -*- coding: utf-8 -*-

from django import forms
from .widgets import SelectWithDisabled
from .models import Offer, OfferImage, Category

from io import BytesIO
from PIL import Image as PilImage
import os
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile


# Function that handles image rezising.
# https://stackoverflow.com/a/58586308/13273250
def resize_uploaded_image(image, max_width, max_height):
    """
    Function that handles image resizing before it's get saved to storage. Used within form's clean methods.
    :param image: Image object.
    :param max_width: Maximum image width.
    :param max_height: Maximum image height.
    :return: Scaled down image object.
    """
    size = (max_width, max_height)

    # Uploaded file is in memory.
    if isinstance(image, InMemoryUploadedFile):
        memory_image = BytesIO(image.read())
        pil_image = PilImage.open(memory_image)
        img_format = os.path.splitext(image.name)[1][1:].upper()
        img_format = 'JPEG' if img_format == 'JPG' else img_format

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)

        new_image = BytesIO()
        pil_image.save(new_image, format=img_format)

        new_image = ContentFile(new_image.getvalue())
        return InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)

    # Uploaded file is in disk.
    elif isinstance(image, TemporaryUploadedFile):
        path = image.temporary_file_path()
        pil_image = PilImage.open(path)

        if pil_image.width > max_width or pil_image.height > max_height:
            pil_image.thumbnail(size)
            pil_image.save(path)
            image.size = os.stat(path).st_size
    return image


class OfferAddForm(forms.ModelForm):
    """
    Form used to add new offers.
    """
    def __init__(self, *args, **kwargs):
        super(OfferAddForm, self).__init__(*args, **kwargs)

        # This snippet handles dropdown choices. It blocks users from using root categories.
        queryset = Category.objects.filter(status=1)
        mptt_opts = queryset.model._mptt_meta
        queryset = queryset.order_by(mptt_opts.tree_id_attr, mptt_opts.left_attr)
        choices = []
        for item in queryset:
            value = Category.objects.get(id=item.id)
            label = item.name
            if item.is_leaf_node():
                choices.append((value, "- " + label))
            else:
                choices.append((value, {'label': label, 'disabled': True}))
        self.fields['category'] = forms.ChoiceField(choices=choices, widget=SelectWithDisabled)

    class Meta:
        model = Offer
        fields = ['title', 'condition', 'price', 'description']


class OfferEditForm(forms.ModelForm):
    """
    Form used to edit already posted offers.
    """
    def __init__(self, *args, **kwargs):
        super(OfferEditForm, self).__init__(*args, **kwargs)

        # This snippet handles dropdown choices. It blocks users from using root categories.
        queryset = Category.objects.filter(status=1)
        mptt_opts = queryset.model._mptt_meta
        queryset = queryset.order_by(mptt_opts.tree_id_attr, mptt_opts.left_attr)
        choices = []
        for item in queryset:
            value = Category.objects.get(id=item.id)
            label = item.name
            if item.is_leaf_node():
                choices.append((value, "- " + label))
            else:
                choices.append((value, {'label': label, 'disabled': True}))
        self.fields['category'] = forms.ChoiceField(choices=choices, widget=SelectWithDisabled)

    class Meta:
        model = Offer
        fields = ['title', 'condition', 'price', 'description']


class OfferSearchForm(forms.ModelForm):
    """
    Form used to search offers.
    """
    class Meta:
        model = Offer
        fields = ['title']
        widgets = {'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Just type some text.'})}


class OfferDeleteForm(forms.ModelForm):
    """
    Form used to set offers inactive.
    """
    class Meta:
        model = Offer
        fields = ['id']


class OfferImageAddForm(forms.ModelForm):
    """
    Form used to add offer images.
    """
    class Meta:
        model = OfferImage
        fields = ['image']
        widgets = {'image': forms.FileInput(attrs={'class': 'custom-file-input', 'style': 'border-radius: 0.25rem;'})}

    img_max_width = 1600
    img_max_height = 900

    def clean_image(self):
        """
        Resize image.
        """
        image = self.cleaned_data.get('image')
        image = resize_uploaded_image(image, self.img_max_width, self.img_max_height)
        return image
