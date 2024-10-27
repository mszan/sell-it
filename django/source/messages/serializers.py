from .models import Conversation, Message
from users.serializers import UserSerializer
from offers.serializers import OfferSerializer
from rest_framework import serializers


class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    """
    Conversation seralizer. Used to obtain basic conversation fields.
    """
    interlocutor_1 = UserSerializer(read_only=True)
    interlocutor_2 = UserSerializer(read_only=True)
    offer = OfferSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'timestamp', 'interlocutor_1', 'interlocutor_2', 'offer', 'messages']
        depth = 1


class MessageSerializer(serializers.ModelSerializer):
    """
    Conversation seralizer. Used to obtain basic message fields.
    """
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'timestamp', 'conversation', 'owner', 'text']
        depth = 1
