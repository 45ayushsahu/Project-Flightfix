from django.db import models


class Aircraft(models.Model):

    STATUS_CHOICES = [
        ("Operational", "Operational"),
        ("Maintenance", "Maintenance"),
        ("Inspection Due", "Inspection Due"),
    ]

    registration_number = models.CharField(
        max_length=20,
        unique=True
    )

    model = models.CharField(
        max_length=100
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Operational"
    )

    last_maintenance = models.DateField(
        null=True,
        blank=True
    )

    next_maintenance = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.registration_number} - {self.model}"


class Maintenance(models.Model):

    MAINTENANCE_STATUS = [
        ("Scheduled", "Scheduled"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Overdue", "Overdue"),
    ]

    aircraft = models.ForeignKey(
        Aircraft,
        on_delete=models.CASCADE,
        related_name="maintenance_records"
    )

    maintenance_type = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    scheduled_date = models.DateField()

    completion_date = models.DateField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=MAINTENANCE_STATUS,
        default="Scheduled"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.aircraft.registration_number} - {self.maintenance_type}"


class Inventory(models.Model):

    part_number = models.CharField(
        max_length=50,
        unique=True
    )

    part_name = models.CharField(
        max_length=100
    )

    category = models.CharField(
        max_length=100
    )

    quantity = models.PositiveIntegerField(
        default=0
    )

    minimum_stock = models.PositiveIntegerField(
        default=5
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def get_status(self):

        if self.quantity == 0:
            return "Out of Stock"

        elif self.quantity <= self.minimum_stock:
            return "Low Stock"

        else:
            return "In Stock"

    def __str__(self):
        return f"{self.part_number} - {self.part_name}"


class Technician(models.Model):

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("On Task", "On Task"),
        ("On Leave", "On Leave"),
    ]

    name = models.CharField(
        max_length=100
    )

    employee_id = models.CharField(
        max_length=50,
        unique=True
    )

    specialization = models.CharField(
        max_length=100
    )

    experience = models.PositiveIntegerField(
        default=0
    )

    current_task = models.CharField(
        max_length=200,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Available"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee_id} - {self.name}"