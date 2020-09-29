from django.urls import path
from messages.views import ConversationView, ConversationListView


urlpatterns = [
    path('conversation/<int:pk>/',
         ConversationView.as_view(),
         name='conversation'),

    path('conversations/',
         ConversationListView.as_view(),
         name='conversations'),
]
