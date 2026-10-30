from django.contrib import admin
from .models import Aircraft, Maintenance, Inventory, Technician


@admin.register(Aircraft)
class AircraftAdmin(admin.ModelAdmin):
    list_display = (
        "registration_number",
        "model",
        "status",
        "last_maintenance",
        "next_maintenance",
    )

    list_filter = ("status",)

    search_fields = (
        "registration_number",
        "model",
    )

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):

    list_display = (
        "aircraft",
        "maintenance_type",
        "scheduled_date",
        "completion_date",
        "status",
    )

    list_filter = (
        "status",
        "maintenance_type",
    )

    search_fields = (
        "aircraft__registration_number",
        "maintenance_type",
        "description",
    )

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):

    list_display = (
        "part_number",
        "part_name",
        "category",
        "quantity",
        "minimum_stock",
        "stock_status",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "part_number",
        "part_name",
        "category",
    )

    def stock_status(self, obj):
        return obj.get_status()

    stock_status.short_description = "Status"

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):

    list_display = (
        "employee_id",
        "name",
        "specialization",
        "experience",
        "current_task",
        "status",
    )

    list_filter = (
        "status",
        "specialization",
    )

    search_fields = (
        "employee_id",
        "name",
        "specialization",
        "current_task",
    )