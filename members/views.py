from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

from .forms import ChurchMemberForm, FamilyForm
from .models import (
    Diocese,
    Deanery,
    Parish,
    SmallChristianCommunity,
    Zone,
    Family,
    ChurchMember,
)


def get_deaneries(request):
    diocese_id = request.GET.get("diocese")

    if not diocese_id:
        return JsonResponse([], safe=False)

    deaneries = (
        Deanery.objects
        .filter(
            diocese_id=diocese_id,
            is_active=True,
        )
        .order_by("name")
    )

    data = [
        {
            "id": str(deanery.id),
            "name": deanery.name,
        }
        for deanery in deaneries
    ]

    return JsonResponse(data, safe=False)


def get_parishes(request):
    deanery_id = request.GET.get("deanery")

    if not deanery_id:
        return JsonResponse([], safe=False)

    parishes = (
        Parish.objects
        .filter(
            deanery_id=deanery_id,
            is_active=True,
        )
        .order_by("name")
    )

    data = [
        {
            "id": str(parish.id),
            "name": parish.name,
        }
        for parish in parishes
    ]

    return JsonResponse(data, safe=False)


def get_zones(request):
    parish_id = request.GET.get("parish")

    if not parish_id:
        return JsonResponse([], safe=False)

    zones = (
        Zone.objects
        .filter(
            parish_id=parish_id,
            is_active=True,
        )
        .order_by("name")
    )

    data = [
        {
            "id": str(zone.id),
            "name": zone.name,
        }
        for zone in zones
    ]

    return JsonResponse(data, safe=False)


def get_small_christian_communities(request):
    zone_id = request.GET.get("zone")

    if not zone_id:
        return JsonResponse([], safe=False)

    communities = (
        SmallChristianCommunity.objects
        .filter(
            zone_id=zone_id,
            is_active=True,
        )
        .order_by("name")
    )

    data = [
        {
            "id": str(community.id),
            "name": community.name,
        }
        for community in communities
    ]

    return JsonResponse(data, safe=False)


def register_family(request):
    if request.method == "POST":
        form = FamilyForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Family registered successfully."
            )

            return redirect("members:register_family")

        messages.warning(
            request,
            "Please correct the errors in the form and try again."
        )

    else:
        form = FamilyForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "members/register_family.html",
        context
    )


@transaction.atomic
def register_member(request):

    if request.method == "POST":

        form = ChurchMemberForm(request.POST)

        if form.is_valid():

            member = form.save(commit=False)

            scc = form.cleaned_data[
                "small_christian_community"
            ]

            family_name = (
                form.cleaned_data
                .get("family", "")
                .strip()
            )

            if family_name:

                family = Family.objects.filter(
                    small_christian_community=scc,
                    name__iexact=family_name,
                    is_active=True,
                ).first()

                if family is None:
                    family = Family.objects.create(
                        small_christian_community=scc,
                        name=family_name,
                        is_active=True,
                    )

                member.family = family.name

            member.save()

            form.save_m2m()

            request.session["pending_member_id"] = str(
                member.pk
            )

            messages.success(
                request,
                "Member registered successfully. "
                "Please complete your account registration.",
            )

            return redirect(
                "accounts:complete_registration"
            )

    else:
        form = ChurchMemberForm()

    return render(
        request,
        "members/register.html",
        {
            "form": form,
        },
    )


@login_required
@never_cache
def dashboard(request):

    try:
        member = request.user.church_member
    except ChurchMember.DoesNotExist:
        member = None

    context = {
        "diocese_count": Diocese.objects.filter(
            is_active=True
        ).count(),

        "deanery_count": Deanery.objects.filter(
            is_active=True
        ).count(),

        "parish_count": Parish.objects.filter(
            is_active=True
        ).count(),

        "zone_count": Zone.objects.filter(
            is_active=True
        ).count(),

        "scc_count": SmallChristianCommunity.objects.filter(
            is_active=True
        ).count(),

        "family_count": Family.objects.filter(
            is_active=True
        ).count(),

        "member_count": ChurchMember.objects.count(),

        # Logged-in user's Church Member profile
        "member": member,
    }

    return render(
        request,
        "members/dashboard.html",
        context,
    )