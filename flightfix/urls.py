from django.contrib import admin
from django.urls import path

from core.views import (
    home,
    dashboard,
    aircraft,
    maintenance,
    inventory,
    inventory_add,
    inventory_edit,
    inventory_delete,
    technicians,
    technician_add,
    technician_edit,
    technician_delete,
    user_login,
    user_logout,
    aircraft_add,
    aircraft_edit,
    aircraft_delete,
    maintenance_add,
    maintenance_edit,
    maintenance_delete,
)


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        home,
        name="home"
    ),

    path(
        "dashboard/",
        dashboard,
        name="dashboard"
    ),

    path(
        "aircraft/",
        aircraft,
        name="aircraft"
    ),

    path(
        "maintenance/",
        maintenance,
        name="maintenance"
    ),

    path(
        "inventory/",
        inventory,
        name="inventory"
    ),

    path(
        "technicians/",
        technicians,
        name="technicians"
    ),

    path(
        "login/",
        user_login,
        name="login"
    ),

    path(
    "logout/",
    user_logout,
    name="logout"
    ),


    # ================= AIRCRAFT =================

    path(
        "aircraft/add/",
        aircraft_add,
        name="aircraft_add"
    ),

    path(
        "aircraft/edit/<int:id>/",
        aircraft_edit,
        name="aircraft_edit"
    ),

    path(
        "aircraft/delete/<int:id>/",
        aircraft_delete,
        name="aircraft_delete"
    ),


    # ================= MAINTENANCE =================

    path(
        "maintenance/add/",
        maintenance_add,
        name="maintenance_add"
    ),

    path(
        "maintenance/edit/<int:id>/",
        maintenance_edit,
        name="maintenance_edit"
    ),

    path(
        "maintenance/delete/<int:id>/",
        maintenance_delete,
        name="maintenance_delete"
    ),

    path(
    "inventory/add/",
    inventory_add,
    name="inventory_add"
    ),

    path(
    "inventory/edit/<int:id>/",
    inventory_edit,
    name="inventory_edit"
    ),

    path(

    "inventory/delete/<int:id>/",

    inventory_delete,

    name="inventory_delete"

    ),  


    path(

    "technicians/add/",

    technician_add,

    name="technician_add"

),


path(
    "technicians/edit/<int:id>/",
    technician_edit,
    name="technician_edit"
),

path(

    "technicians/delete/<int:id>/",

    technician_delete,

    name="technician_delete"

),

]