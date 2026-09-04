from django.urls import path

from . import views

app_name = "members"

urlpatterns = [
    path(
        "register/",
        views.register_member,
        name="register",
    ),

    path(
        "families/register/",
        views.register_family,
        name="register_family",
    ),

    # Hierarchy API endpoints
    path(
        "api/deaneries/",
        views.get_deaneries,
        name="get_deaneries",
    ),

    path(
        "api/parishes/",
        views.get_parishes,
        name="get_parishes",
    ),

    path(
        "api/zones/",
        views.get_zones,
        name="get_zones",
    ),

    path(
        "api/small-christian-communities/",
        views.get_small_christian_communities,
        name="get_small_christian_communities",
    ),
]