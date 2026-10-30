from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import Aircraft,Maintenance, Inventory, Technician
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "core/home.html")

@login_required
def dashboard(request):

    # Aircraft statistics
    total_aircraft = Aircraft.objects.count()

    operational = Aircraft.objects.filter(
        status="Operational"
    ).count()

    under_maintenance = Aircraft.objects.filter(
        status="Maintenance"
    ).count()

    inspection_due = Aircraft.objects.filter(
        status="Inspection Due"
    ).count()


    # Maintenance statistics
    pending_tasks = Maintenance.objects.filter(
        status__in=["Scheduled", "In Progress", "Overdue"]
    ).count()

    upcoming_maintenance = Maintenance.objects.filter(
        status="Scheduled"
    ).order_by("scheduled_date")[:5]
    aircraft_list = Aircraft.objects.all()
    inventory_alerts = Inventory.objects.all().order_by("quantity")[:5]
    


    return render(
        request,
        "core/dashboard.html",
        {
            "total_aircraft": total_aircraft,
            "operational": operational,
            "under_maintenance": under_maintenance,
            "inspection_due": inspection_due,
            "pending_tasks": pending_tasks,
            "upcoming_maintenance": upcoming_maintenance,
            "aircraft_list": aircraft_list,
            "inventory_alerts": inventory_alerts,
        }
    )


@login_required
def aircraft(request):
    search = request.GET.get("search", "")
    status_filter = request.GET.get("status", "")

    aircraft_list = Aircraft.objects.all()

    # Search filter
    if search:
        aircraft_list = aircraft_list.filter(
            Q(registration_number__icontains=search) |
            Q(model__icontains=search) |
            Q(status__icontains=search)
        )

    # Status filter
    if status_filter:
        aircraft_list = aircraft_list.filter(
            status=status_filter
        )

    # Statistics
    total_aircraft = Aircraft.objects.count()
    operational = Aircraft.objects.filter(status="Operational").count()
    maintenance = Aircraft.objects.filter(status="Maintenance").count()
    inspection_due = Aircraft.objects.filter(status="Inspection Due").count()

    return render(
        request,
        "core/aircraft.html",
        {
            "aircraft_list": aircraft_list,
            "total_aircraft": total_aircraft,
            "operational": operational,
            "maintenance": maintenance,
            "inspection_due": inspection_due,
        }
    )
def aircraft_add(request):

    if request.method == "POST":

        registration_number = request.POST.get("registration_number")
        model = request.POST.get("model")
        status = request.POST.get("status")
        last_maintenance = request.POST.get("last_maintenance")
        next_maintenance = request.POST.get("next_maintenance")

        Aircraft.objects.create(
            registration_number=registration_number,
            model=model,
            status=status,
            last_maintenance=last_maintenance or None,
            next_maintenance=next_maintenance or None,
        )

        return redirect("/aircraft/")

    return render(request, "core/add_aircraft.html")

def aircraft_edit(request, id):
    aircraft = Aircraft.objects.get(id=id)

    if request.method == "POST":
        aircraft.registration_number = request.POST.get("registration_number")
        aircraft.model = request.POST.get("model")
        aircraft.status = request.POST.get("status")
        aircraft.last_maintenance = request.POST.get("last_maintenance") or None
        aircraft.next_maintenance = request.POST.get("next_maintenance") or None

        aircraft.save()

        return redirect("/aircraft/")

    return render(
        request,
        "core/edit_aircraft.html",
        {"aircraft": aircraft}
    )

def aircraft_delete(request, id):
    aircraft = Aircraft.objects.get(id=id)

    if request.method == "POST":
        aircraft.delete()
        return redirect("/aircraft/")

    return render(
        request,
        "core/delete_aircraft.html",
        {"aircraft": aircraft}
    )


@login_required
def maintenance(request):
    maintenance_list = Maintenance.objects.all().order_by("scheduled_date")

    total_maintenance = maintenance_list.count()
    scheduled = maintenance_list.filter(status="Scheduled").count()
    in_progress = maintenance_list.filter(status="In Progress").count()
    completed = maintenance_list.filter(status="Completed").count()
    overdue = maintenance_list.filter(status="Overdue").count()

    return render(
        request,
        "core/maintenance.html",
        {
            "maintenance_list": maintenance_list,
            "total_maintenance": total_maintenance,
            "scheduled": scheduled,
            "in_progress": in_progress,
            "completed": completed,
            "overdue": overdue,
        }
    )
def maintenance_add(request):

    if request.method == "POST":

        aircraft_id = request.POST.get("aircraft")
        maintenance_type = request.POST.get("maintenance_type")
        description = request.POST.get("description")
        scheduled_date = request.POST.get("scheduled_date")
        status = request.POST.get("status")

        Maintenance.objects.create(
            aircraft_id=aircraft_id,
            maintenance_type=maintenance_type,
            description=description,
            scheduled_date=scheduled_date,
            status=status,
        )

        return redirect("/maintenance/")

    aircraft_list = Aircraft.objects.all()

    return render(
        request,
        "core/add_maintenance.html",
        {
            "aircraft_list": aircraft_list,
        }
    )

def maintenance_edit(request, id):

    maintenance = Maintenance.objects.get(id=id)

    if request.method == "POST":

        maintenance.aircraft_id = request.POST.get("aircraft")
        maintenance.maintenance_type = request.POST.get("maintenance_type")
        maintenance.description = request.POST.get("description")
        maintenance.scheduled_date = request.POST.get("scheduled_date")
        maintenance.status = request.POST.get("status")

        maintenance.save()

        return redirect("/maintenance/")

    aircraft_list = Aircraft.objects.all()

    return render(
        request,
        "core/edit_maintenance.html",
        {
            "maintenance": maintenance,
            "aircraft_list": aircraft_list,
        }
    )

def maintenance_delete(request, id):

    maintenance = Maintenance.objects.get(id=id)

    if request.method == "POST":
        maintenance.delete()
        return redirect("/maintenance/")

    return render(
        request,
        "core/delete_maintenance.html",
        {
            "maintenance": maintenance,
        }
    )


@login_required
def inventory(request):

    inventory_list = Inventory.objects.all().order_by("part_name")

    total_parts = inventory_list.count()

    in_stock = sum(
        1 for item in inventory_list
        if item.get_status() == "In Stock"
    )

    low_stock = sum(
        1 for item in inventory_list
        if item.get_status() == "Low Stock"
    )

    out_of_stock = sum(
        1 for item in inventory_list
        if item.get_status() == "Out of Stock"
    )

    return render(
        request,
        "core/inventory.html",
        {
            "inventory_list": inventory_list,
            "total_parts": total_parts,
            "in_stock": in_stock,
            "low_stock": low_stock,
            "out_of_stock": out_of_stock,
        }
    )

def inventory_add(request):

    if request.method == "POST":

        part_number = request.POST.get("part_number")
        part_name = request.POST.get("part_name")
        category = request.POST.get("category")
        quantity = request.POST.get("quantity")
        minimum_stock = request.POST.get("minimum_stock")

        Inventory.objects.create(
            part_number=part_number,
            part_name=part_name,
            category=category,
            quantity=quantity,
            minimum_stock=minimum_stock,
        )

        return redirect("/inventory/")

    return render(
        request,
        "core/add_inventory.html"
    )

def inventory_edit(request, id):

    item = Inventory.objects.get(id=id)

    if request.method == "POST":

        item.part_number = request.POST.get("part_number")
        item.part_name = request.POST.get("part_name")
        item.category = request.POST.get("category")
        item.quantity = request.POST.get("quantity")
        item.minimum_stock = request.POST.get("minimum_stock")

        item.save()

        return redirect("/inventory/")

    return render(
        request,
        "core/edit_inventory.html",
        {
            "item": item,
        }
    )

def inventory_delete(request, id):

    item = Inventory.objects.get(id=id)

    if request.method == "POST":
        item.delete()
        return redirect("/inventory/")

    return render(
        request,
        "core/delete_inventory.html",
        {
            "item": item,
        }
    )


@login_required
def technicians(request):

    technician_list = Technician.objects.all().order_by("name")

    total_technicians = technician_list.count()

    available = technician_list.filter(
        status="Available"
    ).count()

    on_task = technician_list.filter(
        status="On Task"
    ).count()

    on_leave = technician_list.filter(
        status="On Leave"
    ).count()

    return render(
        request,
        "core/technicians.html",
        {
            "technician_list": technician_list,
            "total_technicians": total_technicians,
            "available": available,
            "on_task": on_task,
            "on_leave": on_leave,
        }
    )

def technician_add(request):

    if request.method == "POST":

        name = request.POST.get("name")
        employee_id = request.POST.get("employee_id")
        specialization = request.POST.get("specialization")
        experience = request.POST.get("experience")
        current_task = request.POST.get("current_task")
        status = request.POST.get("status")

        Technician.objects.create(
            name=name,
            employee_id=employee_id,
            specialization=specialization,
            experience=experience,
            current_task=current_task,
            status=status,
        )

        return redirect("/technicians/")

    return render(
        request,
        "core/add_technician.html"
    )


def technician_edit(request, id):

    technician = Technician.objects.get(id=id)

    if request.method == "POST":

        technician.name = request.POST.get("name")
        technician.employee_id = request.POST.get("employee_id")
        technician.specialization = request.POST.get("specialization")
        technician.experience = request.POST.get("experience")
        technician.current_task = request.POST.get("current_task")
        technician.status = request.POST.get("status")

        technician.save()

        return redirect("/technicians/")

    return render(
        request,
        "core/edit_technician.html",
        {
            "technician": technician,
        }
    )


def technician_delete(request, id):

    technician = Technician.objects.get(id=id)

    if request.method == "POST":
        technician.delete()
        return redirect("/technicians/")

    return render(
        request,
        "core/delete_technician.html",
        {
            "technician": technician,
        }
    )

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")

        password = request.POST.get("password")

        user = authenticate(

            request,

            username=username,

            password=password

        )

        if user is not None:

            login(request, user)

            return redirect("/dashboard/")

        else:

            from django.contrib import messages

            messages.error(

                request,

                "Invalid username or password."

            )

    return render(request, "core/login.html")


def user_logout(request):
    logout(request)
    return redirect("/login/")