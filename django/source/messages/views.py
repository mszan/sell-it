from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from .forms import MessageSendForm
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationView(LoginRequiredMixin, ListView):
    """
    Conversation view used to list conversation's messages and send new messages.
    """
    model = Conversation
    template_name = 'messages/conversation.html'

    def get(self, request, *args, **kwargs):
        conversation = Conversation.objects.get(id=self.kwargs.get('pk'))
        interlocutors = [conversation.interlocutor_1, conversation.interlocutor_2]
        if self.request.user not in interlocutors:
            messages.warning(request, 'You are not allowed to see this conversation.')
            return redirect('offers-home')

        context = self.get_context_data()
        context['message_send_form'] = MessageSendForm()
        return render(request, 'messages/conversation.html', context)

    def post(self, request, *args, **kwargs):
        conversation = Conversation.objects.get(id=self.kwargs.get('pk'))
        interlocutors = [conversation.interlocutor_1, conversation.interlocutor_2]
        if self.request.user not in interlocutors:
            messages.warning(request, 'You are not allowed to send a message in this conversation.')
            return redirect('offers-home')

        message_send_form = MessageSendForm(request.POST)
        if message_send_form.is_valid():
            message = message_send_form.save(commit=False)
            message.owner = request.user
            message.conversation = Conversation.objects.get(id=self.kwargs.get('pk'))
            message.save()

            messages.info(request, 'Message sent!')
            return redirect('conversation', pk=message.conversation.id)
        context = self.get_context_data()
        return render(request, 'messages/conversation.html', context)

    def get_context_data(self, **kwargs):
        conversation = Conversation.objects.get(id=self.kwargs.get('pk'))
        interlocutors = [conversation.interlocutor_1, conversation.interlocutor_2]
        recipient = interlocutors[1] if interlocutors[0] == self.request.user else interlocutors[0]
        user_messages = Message.objects.filter(conversation=conversation)

        context = {'page_title': 'Conversation ID' + str(conversation.id), 'conversation': conversation,
                   'user_messages': user_messages, 'recipient': recipient, }

        return context


class ConversationListView(LoginRequiredMixin, ListView):
    """
    Conversation list view used to list user's conversations.
    """
    model = Conversation
    template_name = 'messages/conversation_list.html'
    context_object_name = 'conversations'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        conversations = Conversation.objects.filter(
            Q(interlocutor_1=self.request.user) | Q(interlocutor_2=self.request.user))
        for conversation in conversations:
            conversation.last_message = Message.objects.filter(conversation=conversation).last()
        return conversations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Conversations'
        return context


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Overrided in order to return list of user's messages unless it's staff user or superuser.
        """
        queryset = Conversation.objects.all()
        if not request.user.is_staff or not request.user.is_superuser:
            queryset = Conversation.objects.filter(Q(interlocutor_1=request.user) | Q(interlocutor_2=request.user))
        serializer = ConversationSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        Overrided in order to return list of user's messages unless it's staff user or superuser.
        """
        queryset = Message.objects.all()
        if not request.user.is_staff or not request.user.is_superuser:
            queryset = Message.objects.filter(Q(conversation__interlocutor_1=request.user) | Q(conversation__interlocutor_2=request.user))
        serializer = ConversationSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)
