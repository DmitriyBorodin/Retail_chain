from rest_framework import serializers
from .models import Entity


class EntitySerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Entity
        fields = [
            "id",
            "name",
            "entity_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "hierarchy_level",
            "debt",
            "created_at",
        ]
        read_only_fields = ["debt", "hierarchy_level", "created_at"]
