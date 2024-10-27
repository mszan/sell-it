# Generated by Django 3.1 on 2024-10-27 17:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('interlocutor_1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interlocutor_1', to=settings.AUTH_USER_MODEL)),
                ('interlocutor_2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='interlocutor_2', to=settings.AUTH_USER_MODEL)),
                ('offer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='offers.offer')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='user_messages.conversation')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]