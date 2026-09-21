from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from accounts.permissions import require_role
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import PermissionDenied
from accounts.permissions import can_manage_members

from .forms import (
    ChurchAssociationForm,
    ChurchMemberForm,
    FamilyForm,
    MemberAssociationForm,
    LeadershipPositionForm,
    MemberLeadershipForm,
)

from .models import (
    Diocese,
    Deanery,
    Parish,
    SmallChristianCommunity,
    Zone,
    Family,
    ChurchMember,
    ChurchAssociation,
    LeadershipPosition,
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

@login_required
@never_cache
def association_list(request):
    associations = ChurchAssociation.objects.all().order_by("name")

    context = {
        "associations": associations,
    }

    return render(
        request,
        "members/associations/list.html",
        context,
    )


@login_required
@never_cache
@require_role("diocese_admin")
def association_create(request):
    if request.method == "POST":
        form = ChurchAssociationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Church association created successfully."
            )

            return redirect("members:association_list")

    else:
        form = ChurchAssociationForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "members/associations/form.html",
        context,
    )


@login_required
@never_cache
@require_role("diocese_admin")
def association_update(request, pk):
    association = get_object_or_404(ChurchAssociation, pk=pk)
    if request.method == "POST":
        form = ChurchAssociationForm(
            request.POST,
            instance=association,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Church association updated successfully."
            )

            return redirect("members:association_list")

    else:
        form = ChurchAssociationForm(instance=association)

    context = {
        "form": form,
        "association": association,
    }

    return render(
        request,
        "members/associations/form.html",
        context,
    )

@login_required
@never_cache
def member_associations(request, pk):

    if not can_manage_members(request.user):
        raise PermissionDenied

    member = get_object_or_404(
        ChurchMember,
        pk=pk
    )

    if request.method == "POST":

        form = MemberAssociationForm(
            request.POST,
            instance=member
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Member associations updated successfully."
            )

            return redirect(
                "members:member_associations",
                pk=member.pk
            )

    else:

        form = MemberAssociationForm(
            instance=member
        )

    return render(
        request,
        "members/member_associations.html",
        {
            "member": member,
            "form": form,
        }
    )

@login_required
@never_cache
def leadership_list(request):
    positions = LeadershipPosition.objects.all().order_by("name")

    context = {
        "positions": positions,
    }

    return render(
        request,
        "members/leadership/list.html",
        context,
    )


@login_required
@never_cache
@require_role("diocese_admin")
def leadership_create(request):

    if request.method == "POST":
        form = LeadershipPositionForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Leadership position created successfully."
            )

            return redirect("members:leadership_list")

    else:
        form = LeadershipPositionForm()

    context = {
        "form": form,
    }

    return render(
        request,
        "members/leadership/form.html",
        context,
    )


@login_required
@never_cache
@require_role("diocese_admin")
def leadership_update(request, pk):

    position = get_object_or_404(
        LeadershipPosition,
        pk=pk
    )

    if request.method == "POST":
        form = LeadershipPositionForm(
            request.POST,
            instance=position,
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Leadership position updated successfully."
            )

            return redirect("members:leadership_list")

    else:
        form = LeadershipPositionForm(
            instance=position
        )

    context = {
        "form": form,
        "position": position,
    }

    return render(
        request,
        "members/leadership/form.html",
        context,
    )

@login_required
@never_cache
def member_leadership(request, pk):

    if not can_manage_members(request.user):
        raise PermissionDenied

    member = get_object_or_404(
        ChurchMember,
        pk=pk
    )

    if request.method == "POST":

        form = MemberLeadershipForm(
            request.POST,
            instance=member
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Member leadership positions updated successfully."
            )

            return redirect(
                "members:member_leadership",
                pk=member.pk
            )

    else:

        form = MemberLeadershipForm(
            instance=member
        )

    return render(
        request,
        "members/member_leadership.html",
        {
            "member": member,
            "form": form,
        }
    )