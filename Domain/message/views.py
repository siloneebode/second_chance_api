from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action

from Domain.account.models import User
from Domain.conversation.models import Conversation
from Domain.conversation.serializers import ConversationSerializer
from Domain.message.models import Message
from Domain.message.serializers import MessageSerializer


class MessageView(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        queryset = Message.objects.all()
        conversation_id = self.request.query_params.get('conversation')
        if conversation_id is not None:
            queryset = queryset.filter(conversation=conversation_id)

        return queryset

    def perform_create(self, serializer):
        # TODO: ici on doit vérifier qu'il existe deja une conversation entre les deux sinon on crée une nouvelle
        if Conversation.objects.raw('SELECT * FROM conversation_conversation WHERE conversation_conversation.author = %s OR conversation_conversation.receiver = %s' % self.request.user):
            pass

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)

        return JsonResponse({'data': serializer.validated_data, 'message': 'message envoyé avec succès'},
                            status=status.HTTP_201_CREATED)

    @action(['POST'], detail=True)
    def create_without_conversation(self, request, receiver_id):
        receiver = User.objects.filter(pk=receiver_id)
        if receiver.exist():
            conversation = Conversation.objects.create(
                author=request.user,
                receiver=receiver,
                sticky=False
            )

            conversation.save()
            serializer = self.serializer_class(data=request.data)

