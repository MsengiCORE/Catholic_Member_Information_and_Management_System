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
        "register-family/",
        views.register_family,
        name="register_family",
    ),

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

    path(
        "dashoard/",
        views.dashboard,
        name="dashboard",
    ),
    
    path(
        "associations/",
        views.association_list,
        name="association_list",
    ),

    path(
        "associations/create/",
        views.association_create,
        name="association_create",
    ),

    path(
        "associations/<uuid:pk>/edit/",
        views.association_update,
        name="association_update",
    ),

    path(
        "members/<uuid:pk>/associations/",
        views.member_associations,
        name="member_associations",
    ),

    path(
        "leadership/",
        views.leadership_list,
        name="leadership_list",
    ),

    path(
        "leadership/create/",
        views.leadership_create,
        name="leadership_create",
    ),

    path(
        "leadership/<uuid:pk>/edit/",
        views.leadership_update,
        name="leadership_update",
    ),

    path(
        "members/<uuid:pk>/leadership/",
        views.member_leadership,
        name="member_leadership",
    ),
]