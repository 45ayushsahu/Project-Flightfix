from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date

from .models import Aircraft, Maintenance, Inventory, Technician


class FlightFixAutomatedTests(TestCase):
    """
    Automated functional tests for the FlightFix Django application.

    Test data is intentionally created inside the test database, so the
    real development database is NOT modified.
    """

    @classmethod
    def setUpTestData(cls):
        # -------------------------
        # Test user
        # -------------------------
        cls.user = User.objects.create_user(
            username="flightfix_test_user",
            password="Test@12345"
        )

        # -------------------------
        # Aircraft test dataset
        # -------------------------
        cls.aircraft_operational = Aircraft.objects.create(
            registration_number="FFX-T001",
            model="Boeing 737",
            status="Operational",
            last_maintenance=date(2026, 8, 1),
            next_maintenance=date(2026, 11, 1),
        )

        cls.aircraft_maintenance = Aircraft.objects.create(
            registration_number="FFX-T002",
            model="Airbus A320",
            status="Maintenance",
            last_maintenance=date(2026, 7, 15),
            next_maintenance=date(2026, 10, 15),
        )

        cls.aircraft_inspection = Aircraft.objects.create(
            registration_number="FFX-T003",
            model="Boeing 777",
            status="Inspection Due",
            last_maintenance=date(2026, 6, 10),
            next_maintenance=date(2026, 10, 5),
        )

        # -------------------------
        # Maintenance test dataset
        # -------------------------
        cls.maintenance_scheduled = Maintenance.objects.create(
            aircraft=cls.aircraft_operational,
            maintenance_type="Routine Inspection",
            description="Automated test scheduled maintenance task",
            scheduled_date=date(2026, 10, 10),
            status="Scheduled",
        )

        cls.maintenance_progress = Maintenance.objects.create(
            aircraft=cls.aircraft_maintenance,
            maintenance_type="Engine Check",
            description="Automated test in-progress task",
            scheduled_date=date(2026, 9, 30),
            status="In Progress",
        )

        cls.maintenance_overdue = Maintenance.objects.create(
            aircraft=cls.aircraft_inspection,
            maintenance_type="Safety Inspection",
            description="Automated test overdue task",
            scheduled_date=date(2026, 9, 20),
            status="Overdue",
        )

        # -------------------------
        # Inventory test dataset
        # -------------------------
        cls.inventory_normal = Inventory.objects.create(
            part_number="FFX-P001",
            part_name="Engine Filter",
            category="Engine",
            quantity=25,
            minimum_stock=10,
        )

        cls.inventory_low = Inventory.objects.create(
            part_number="FFX-P002",
            part_name="Brake Assembly",
            category="Brake",
            quantity=5,
            minimum_stock=10,
        )

        cls.inventory_out = Inventory.objects.create(
            part_number="FFX-P003",
            part_name="Hydraulic Pump",
            category="Hydraulic",
            quantity=0,
            minimum_stock=5,
        )

        # -------------------------
        # Technician test dataset
        # -------------------------
        cls.tech_available = Technician.objects.create(
            name="Test Technician One",
            employee_id="FFX-EMP001",
            specialization="Engine",
            experience="5",
            current_task="Routine Inspection",
            status="Available",
        )

        cls.tech_on_task = Technician.objects.create(
            name="Test Technician Two",
            employee_id="FFX-EMP002",
            specialization="Avionics",
            experience="4",
            current_task="Engine Check",
            status="On Task",
        )

        cls.tech_on_leave = Technician.objects.create(
            name="Test Technician Three",
            employee_id="FFX-EMP003",
            specialization="Structural",
            experience="6",
            current_task="Leave",
            status="On Leave",
        )

    def setUp(self):
        self.client = Client()

    # ==========================================================
    # AUTHENTICATION TESTS
    # ==========================================================

    def test_valid_login(self):
        response = self.client.post(
            "/login/",
            {"username": "flightfix_test_user", "password": "Test@12345"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/dashboard/")

    def test_invalid_login(self):
        response = self.client.post(
            "/login/",
            {"username": "flightfix_test_user", "password": "WrongPassword"},
        )
        self.assertEqual(response.status_code, 200)

        self.client.login(
            username="flightfix_test_user",
            password="Test@12345"
        )
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login/")

    # ==========================================================
    # AIRCRAFT TESTS
    # ==========================================================

    def test_aircraft_count(self):
        self.assertEqual(Aircraft.objects.count(), 3)

    def test_aircraft_status_counts(self):
        self.assertEqual(
            Aircraft.objects.filter(status="Operational").count(), 1
        )
        self.assertEqual(
            Aircraft.objects.filter(status="Maintenance").count(), 1
        )
        self.assertEqual(
            Aircraft.objects.filter(status="Inspection Due").count(), 1
        )

    def test_aircraft_search(self):

        self.client.login(

        username="flightfix_test_user",

        password="Test@12345"

    )

        response = self.client.get(

        "/aircraft/",

        {"search": "FFX-T002"}

    )

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "FFX-T002")

        self.assertNotContains(response, "FFX-T001")

    def test_aircraft_status_filter(self):
        self.client.login(
        username="flightfix_test_user",
        password="Test@12345"
    )

        response = self.client.get(
        "/aircraft/",
        {"status": "Maintenance"}
    )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FFX-T002")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "FFX-T002")

    def test_aircraft_create(self):
        aircraft = Aircraft.objects.create(
            registration_number="FFX-T004",
            model="Airbus A350",
            status="Operational",
            last_maintenance=date(2026, 9, 1),
            next_maintenance=date(2026, 12, 1),
        )
        self.assertTrue(
            Aircraft.objects.filter(
                registration_number="FFX-T004"
            ).exists()
        )
        self.assertEqual(aircraft.status, "Operational")

    def test_aircraft_update(self):
        aircraft = Aircraft.objects.get(
            registration_number="FFX-T001"
        )
        aircraft.status = "Maintenance"
        aircraft.save()

        aircraft.refresh_from_db()
        self.assertEqual(aircraft.status, "Maintenance")

    def test_aircraft_delete(self):
        aircraft = Aircraft.objects.get(
            registration_number="FFX-T003"
        )
        aircraft.delete()

        self.assertFalse(
            Aircraft.objects.filter(
                registration_number="FFX-T003"
            ).exists()
        )

    # ==========================================================
    # MAINTENANCE TESTS
    # ==========================================================

    def test_maintenance_count(self):
        self.assertEqual(Maintenance.objects.count(), 3)

    def test_pending_maintenance_count(self):
        pending = Maintenance.objects.filter(
            status__in=["Scheduled", "In Progress", "Overdue"]
        ).count()
        self.assertEqual(pending, 3)

    def test_maintenance_aircraft_relationship(self):
        maintenance = Maintenance.objects.get(
            description="Automated test scheduled maintenance task"
        )
        self.assertEqual(
            maintenance.aircraft.registration_number,
            "FFX-T001"
        )

    def test_maintenance_status_update(self):
        maintenance = self.maintenance_scheduled
        maintenance.status = "Completed"
        maintenance.save()

        maintenance.refresh_from_db()
        self.assertEqual(maintenance.status, "Completed")

    # ==========================================================
    # INVENTORY TESTS
    # ==========================================================

    def test_inventory_count(self):
        self.assertEqual(Inventory.objects.count(), 3)

    def test_inventory_status_logic(self):
        self.assertEqual(
            self.inventory_normal.get_status(),
            "In Stock"
        )
        self.assertEqual(
            self.inventory_low.get_status(),
            "Low Stock"
        )
        self.assertEqual(
            self.inventory_out.get_status(),
            "Out of Stock"
        )

    def test_inventory_update(self):
        item = self.inventory_normal
        item.quantity = 5
        item.save()

        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.get_status(), "Low Stock")

    def test_inventory_zero_quantity(self):
        self.assertEqual(self.inventory_out.quantity, 0)
        self.assertEqual(
            self.inventory_out.get_status(),
            "Out of Stock"
        )

    # ==========================================================
    # TECHNICIAN TESTS
    # ==========================================================

    def test_technician_count(self):
        self.assertEqual(Technician.objects.count(), 3)

    def test_technician_status_counts(self):
        self.assertEqual(
            Technician.objects.filter(status="Available").count(), 1
        )
        self.assertEqual(
            Technician.objects.filter(status="On Task").count(), 1
        )
        self.assertEqual(
            Technician.objects.filter(status="On Leave").count(), 1
        )

    def test_technician_create(self):
        technician = Technician.objects.create(
            name="Test Technician Four",
            employee_id="FFX-EMP004",
            specialization="Hydraulics",
            experience="3",
            current_task="Inspection",
            status="Available",
        )

        self.assertTrue(
            Technician.objects.filter(
                employee_id="FFX-EMP004"
            ).exists()
        )
        self.assertEqual(technician.status, "Available")

    # ==========================================================
    # PAGE ACCESS TESTS
    # ==========================================================

    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_dashboard_after_login(self):
        self.client.login(
            username="flightfix_test_user",
            password="Test@12345"
        )

        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)

    def test_aircraft_page_after_login(self):
        self.client.login(
            username="flightfix_test_user",
            password="Test@12345"
        )

        response = self.client.get("/aircraft/")
        self.assertEqual(response.status_code, 200)

    def test_maintenance_page_after_login(self):
        self.client.login(
            username="flightfix_test_user",
            password="Test@12345"
        )

        response = self.client.get("/maintenance/")
        self.assertEqual(response.status_code, 200)

    def test_inventory_page_after_login(self):
        self.client.login(
            username="flightfix_test_user",
            password="Test@12345"
        )

        response = self.client.get("/inventory/")
        self.assertEqual(response.status_code, 200)

    def test_technicians_page_after_login(self):
        self.client.login(
            username="flightfix_test_user",
            password="Test@12345"
        )

        response = self.client.get("/technicians/")
        self.assertEqual(response.status_code, 200)
