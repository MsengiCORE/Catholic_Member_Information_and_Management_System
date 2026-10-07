from django.urls import path

from . import views


app_name = "member_requests"


urlpatterns = [
    # ============================================================
    # Marriage Requests
    # ============================================================

    path(
        "marriage/",
        views.marriage_request_list,
        name="marriage_list",
    ),

    path(
        "marriage/create/",
        views.marriage_request_create,
        name="marriage_create",
    ),

    path(
        "marriage/<uuid:pk>/",
        views.marriage_request_detail,
        name="marriage_detail",
    ),

    path(
        "marriage/<uuid:pk>/review/",
        views.marriage_request_start_review,
        name="marriage_start_review",
    ),

    path(
        "marriage/<uuid:pk>/approve/",
        views.marriage_request_approve,
        name="marriage_approve",
    ),

    path(
        "marriage/<uuid:pk>/reject/",
        views.marriage_request_reject,
        name="marriage_reject",
    ),

    # ============================================================
    # Transfer Requests
    # ============================================================

    path(
        "transfer/",
        views.transfer_request_list,
        name="transfer_list",
    ),

    path(
        "transfer/create/",
        views.transfer_request_create,
        name="transfer_create",
    ),

    path(
        "transfer/<uuid:pk>/",
        views.transfer_request_detail,
        name="transfer_detail",
    ),

    path(
        "transfer/<uuid:pk>/review/",
        views.transfer_request_start_review,
        name="transfer_start_review",
    ),

    path(
        "transfer/<uuid:pk>/approve/",
        views.transfer_request_approve,
        name="transfer_approve",
    ),

    path(
        "transfer/<uuid:pk>/reject/",
        views.transfer_request_reject,
        name="transfer_reject",
    ),

    # ============================================================
    # Travel Certificate Requests
    # ============================================================

    path(
        "travel-certificate/",
        views.travel_certificate_request_list,
        name="travel_certificate_list",
    ),

    path(
        "travel-certificate/create/",
        views.travel_certificate_request_create,
        name="travel_certificate_create",
    ),

    path(
        "travel-certificate/<uuid:pk>/",
        views.travel_certificate_request_detail,
        name="travel_certificate_detail",
    ),

    path(
        "travel-certificate/<uuid:pk>/review/",
        views.travel_certificate_request_start_review,
        name="travel_certificate_start_review",
    ),

    path(
        "travel-certificate/<uuid:pk>/approve/",
        views.travel_certificate_request_approve,
        name="travel_certificate_approve",
    ),

    path(
        "travel-certificate/<uuid:pk>/reject/",
        views.travel_certificate_request_reject,
        name="travel_certificate_reject",
    ),
]