from django.urls import path
from . import views

app_name = "members"

urlpatterns = [
    path("view-members/", views.member_list, name="member_list"),
    path("view-members/data/", views.member_data, name="member_data"),
    path("member-details/<uuid:pk>/", views.member_detail, name="member_detail"),
    path("member-info/<uuid:pk>/edit/", views.member_update, name="member_update"),

    path("register/", views.register_member, name="register"),
    path("register-new-member/", views.register_new_member, name="register_new_member"),

    path("dioceses/", views.diocese_list, name="diocese_list"),
    path("dioceses/data/", views.diocese_data, name="diocese_data"),
    path("dioceses/create/", views.diocese_create, name="diocese_create"),
    path("dioceses/<uuid:pk>/edit/", views.diocese_update, name="diocese_update"),
    path("dioceses/<uuid:pk>/toggle-status/", views.diocese_toggle_status, name="diocese_toggle_status"),

    path("deaneries/", views.deanery_list, name="deanery_list"),
    path("deaneries/data/", views.deanery_data, name="deanery_data"),
    path("deaneries/create/", views.deanery_create, name="deanery_create"),
    path("deaneries/<uuid:pk>/edit/", views.deanery_update, name="deanery_update"),

    path("parishes/", views.parish_list, name="parish_list"),
    path("parishes/data/", views.parish_data, name="parish_data"),
    path("parishes/create/", views.parish_create, name="parish_create"),
    path("parishes/<uuid:pk>/edit/", views.parish_update, name="parish_update"),

    path("zones/", views.zone_list, name="zone_list"),
    path("zones/data/", views.zone_data, name="zone_data"),
    path("zones/create/", views.zone_create, name="zone_create"),
    path("zones/<uuid:pk>/edit/", views.zone_update, name="zone_update"),

    path("small-christian-communities/", views.small_christian_community_list, name="small_christian_community_list"),
    path("small-christian-communities/data/", views.small_christian_community_data, name="small_christian_community_data"),
    path("small-christian-communities/create/", views.small_christian_community_create, name="small_christian_community_create"),
    path("small-christian-communities/<uuid:pk>/edit/", views.small_christian_community_update, name="small_christian_community_update"),

    path("families/", views.family_list, name="family_list"),
    path("families/data/", views.family_data, name="family_data"),
    path("families/create/", views.family_create, name="family_create"),
    path("families/<uuid:pk>/edit/", views.family_update, name="family_update"),

    path("api/deaneries/", views.get_deaneries, name="get_deaneries"),
    path("api/parishes/", views.get_parishes, name="get_parishes"),
    path("api/zones/", views.get_zones, name="get_zones"),
    path("api/small-christian-communities/", views.get_small_christian_communities, name="get_small_christian_communities"),

    path("dashoard/", views.dashboard, name="dashboard"),
    
    path("associations/", views.association_list, name="association_list"),
    path("associations/create/", views.association_create, name="association_create"),
    path("associations/<uuid:pk>/edit/", views.association_update, name="association_update"),
    path("member-associations/<uuid:pk>/associations/", views.member_associations, name="member_associations"),

    path("leadership/", views.leadership_list, name="leadership_list"),
    path("leadership/create/", views.leadership_create, name="leadership_create"),
    path("leadership/<uuid:pk>/edit/", views.leadership_update, name="leadership_update"),
    path("member-leadership/<uuid:pk>/leadership/", views.member_leadership, name="member_leadership"),
]