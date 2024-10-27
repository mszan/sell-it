# Generated by Django 3.1 on 2024-10-27 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import offers.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Not active')])),
                ('name', models.CharField(max_length=25)),
                ('url', models.CharField(max_length=25)),
                ('desc', models.CharField(blank=True, max_length=400)),
                ('thumbnail', models.ImageField(default='images/offers/no_image.png', upload_to='images/offers/categories')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='child', to='offers.category')),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Not active')], default=1)),
                ('title', models.CharField(max_length=50)),
                ('price', models.PositiveIntegerField()),
                ('condition', models.IntegerField(choices=[(1, 'Brand new'), (2, 'Renewed'), (3, 'Used - very good'), (4, 'Used - good'), (5, 'Used - acceptable')])),
                ('description', models.CharField(max_length=2000)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='offers.category')),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='images/offers/no_image.png', upload_to=offers.models.offer_image_upload_path)),
                ('index', models.IntegerField(default=1)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='offer_images', to='offers.offer')),
            ],
            options={
                'verbose_name_plural': 'Offer Images',
            },
        ),
    ]