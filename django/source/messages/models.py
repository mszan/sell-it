# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

from offers.models import Offer


class Conversation(models.Model):
    """
    Conversation model.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    interlocutor_1 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='interlocutor_1')
    interlocutor_2 = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='interlocutor_2')
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True)     # Related user offer.

    def __str__(self):
        return f'Conversation {self.id} for offer {self.offer.id};'


class Message(models.Model):
    """
    Message model.
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    text = models.TextField(null=False)     # Message's text.

    def __str__(self):
        return f'Message {self.conversation.id} sent by {self.owner}; {self.text}'