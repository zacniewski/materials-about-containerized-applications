from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all().order_by('-created_at')
    serializer_class = TodoSerializer

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        todo = self.get_object()
        todo.completed = not todo.completed
        todo.save()
        return Response(self.get_serializer(todo).data)
