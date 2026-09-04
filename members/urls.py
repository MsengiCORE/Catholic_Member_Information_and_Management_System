from django.urls import path

from . import views


app_name = "members"


urlpatterns = [
    path(
        "register/",
        views.register_member,
        name="register",
    ),
]