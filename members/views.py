from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import ChurchMemberForm, FamilyForm
from .models import (
    Deanery,
    Parish,
    SmallChristianCommunity,
    Zone,
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

def register_member(request):
    if request.method == "POST":
        form = ChurchMemberForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Church member registered successfully."
            )

            return redirect("members:register")

    else:
        form = ChurchMemberForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "members/register.html",
        context
    )