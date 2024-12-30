from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from tech_net.models import Entity, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(self, request, queryset):
    updated = queryset.update(debt=0.00)
    self.message_user(request, f"Задолженность успешно очищена у {updated} объектов.")

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'entity_type', 'city', 'supplier_link', 'debt', 'created_at', 'hierarchy_level')
    list_filter = ('city',)
    actions = [clear_debt]

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:tech_net_entity_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return "Нет поставщика"
    supplier_link.short_description = "Поставщик"


@admin.register(Product)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'release_date', 'organization')
