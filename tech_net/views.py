from rest_framework import viewsets, filters
from users.permissions import IsActiveStaff
from .models import Entity
from .serializers import EntitySerializer


class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    permission_classes = [
        IsActiveStaff
    ]  # Ограничение доступа только для авторизованных пользователей
    filter_backends = [filters.SearchFilter]  # Подключение фильтров
    search_fields = ["country"]  # Добавление фильтрации по стране

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        # Поле "debt" игнорируется даже если передано
        serializer.save(debt=self.get_object().debt)
