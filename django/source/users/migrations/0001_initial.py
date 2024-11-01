# Generated by Django 3.1 on 2024-10-27 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_online', models.BooleanField(default=0)),
                ('voivodeship', models.IntegerField(choices=[(1, 'wielkopolskie'), (2, 'kujawsko-pomorskie'), (3, 'małopolskie'), (4, 'łódzkie'), (5, 'dolnośląskie'), (6, 'lubelskie'), (7, 'lubuskie'), (8, 'mazowieckie'), (9, 'opolskie'), (10, 'podlaskie'), (11, 'śląskie'), (12, 'podkarpackie'), (13, 'świętokrzyskie'), (14, 'warmińsko-mazurskie'), (15, 'zachodniopomorskie')], null=True)),
                ('phone_number', models.PositiveIntegerField(null=True)),
                ('phone_number_visible', models.BooleanField(default=0)),
                ('profile_picture', models.ImageField(default='images/users/no_image.png', upload_to=users.models.offer_image_upload_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
