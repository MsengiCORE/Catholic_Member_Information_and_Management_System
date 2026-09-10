from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from django.contrib import messages

from members.models import ChurchMember

from .forms import (
    LoginForm,
    CompleteRegistrationForm,
)


def login_view(request):
    """
    Authenticate an existing CCMIMS user.
    """

    if request.user.is_authenticated:
        return redirect("members:dashboard")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            login(request, user)

            remember_me = request.POST.get("remember_me")

            if remember_me:
                request.session.set_expiry(None)
            else:
                request.session.set_expiry(0)

            return redirect("members:dashboard")

    else:
        form = LoginForm()

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
        },
    )


def complete_registration(request):
    """
    Complete registration for a newly registered church member.

    The phone number becomes the Django username.
    """

    pending_member_id = request.session.get("pending_member_id")

    if not pending_member_id:
        messages.warning(
            request,
            "Your registration session has expired. "
            "Please register again."
        )
        return redirect("members:register")

    try:
        member = ChurchMember.objects.get(
            pk=pending_member_id
        )
    except ChurchMember.DoesNotExist:
        request.session.pop("pending_member_id", None)

        messages.error(
            request,
            "The member registration could not be found."
        )

        return redirect("members:register")

    if member.user is not None:
        request.session.pop("pending_member_id", None)

        messages.info(
            request,
            "This member already has an account."
        )

        return redirect("accounts:login")

    if request.method == "POST":
        form = CompleteRegistrationForm(request.POST)

        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password1"]

            user = User.objects.create_user(
                username=phone_number,
                password=password,
            )

            member.phone_number = phone_number
            member.user = user
            member.save(
                update_fields=[
                    "phone_number",
                    "user",
                    "updated_at",
                ]
            )

            request.session.pop(
                "pending_member_id",
                None
            )

            messages.success(
                request,
                "Registration completed successfully. "
                "You can now log in using your phone number."
            )

            return redirect("accounts:login")

    else:
        form = CompleteRegistrationForm()

    return render(
        request,
        "accounts/complete_registration.html",
        {
            "form": form,
            "member": member,
        },
    )


@never_cache
@login_required
def dashboard_redirect(request):
    return redirect("members:dashboard")

def logout_view(request):
    """
    Log the current user out of CCMIMS.
    """
    logout(request)

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect("accounts:login")