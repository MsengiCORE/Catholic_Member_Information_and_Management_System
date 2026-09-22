from django.db import transaction
from django.db.models import Q

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

from accounts.permissions import (
    can_access_member,
    can_manage_members,
    get_accessible_members,
    is_church_member,
    can_access_scc,
)

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


@login_required
@never_cache
def register_family(request):
    if request.method == "POST":
        form = FamilyForm(request.POST)

        if form.is_valid():
            scc = form.cleaned_data["small_christian_community"]

            if not can_access_scc(request.user, scc):
                raise PermissionDenied

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

            member.small_christian_community = scc

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
@transaction.atomic
def register_new_member(request):

    if request.method == "POST":

        form = ChurchMemberForm(request.POST)

        if form.is_valid():

            member = form.save(commit=False)

            scc = form.cleaned_data[
                "small_christian_community"
            ]

            if not can_access_scc(request.user, scc):
                raise PermissionDenied

            member.small_christian_community = scc

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
                "Please complete member account registration.",
            )

            return redirect(
                "accounts:complete_new_member_registration"
            )

    else:
        form = ChurchMemberForm()

    return render(
        request,
        "members/register_new_member.html",
        {
            "form": form,
        },
    )


@login_required
@never_cache
def member_list(request):
    if not can_manage_members(request.user) and not is_church_member(request.user):
        raise PermissionDenied

    query = request.GET.get("q", "").strip()

    diocese_id = request.GET.get("diocese", "").strip()
    deanery_id = request.GET.get("deanery", "").strip()
    parish_id = request.GET.get("parish", "").strip()
    zone_id = request.GET.get("zone", "").strip()
    scc_id = request.GET.get("scc", "").strip()
    family_name = request.GET.get("family", "").strip()

    members = ChurchMember.objects.select_related(
        "small_christian_community__zone__parish__deanery__diocese"
    ).all()

    members = get_accessible_members(
        request.user,
        members,
    )

    # ---------------------------------------------------------
    # Text search
    # ---------------------------------------------------------
    if query:
        members = members.filter(
            Q(digital_offering_number__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(email__icontains=query)
        )

    # ---------------------------------------------------------
    # Organizational filters
    # ---------------------------------------------------------
    if diocese_id:
        members = members.filter(
            small_christian_community__zone__parish__deanery__diocese_id=diocese_id
        )

    if deanery_id:
        members = members.filter(
            small_christian_community__zone__parish__deanery_id=deanery_id
        )

    if parish_id:
        members = members.filter(
            small_christian_community__zone__parish_id=parish_id
        )

    if zone_id:
        members = members.filter(
            small_christian_community__zone_id=zone_id
        )

    if scc_id:
        members = members.filter(
            small_christian_community_id=scc_id
        )

    # ---------------------------------------------------------
    # Family filter
    # Family is intentionally a CharField.
    # ---------------------------------------------------------
    members = members.order_by(
        "last_name",
        "first_name",
        "middle_name",
    )

    # Keep the queryset before applying the family filter
    # so that the family dropdown can be populated correctly.
    family_members = members

    if family_name:
        members = members.filter(
            family__iexact=family_name
        )

    # ---------------------------------------------------------
    # Filter option querysets
    # Respect the user's organizational scope.
    # ---------------------------------------------------------

    profile = None

    if not request.user.is_superuser:
        from accounts.permissions import get_user_profile

        profile = get_user_profile(request.user)


    # ---------------------------------------------------------
    # Diocese filter
    # ---------------------------------------------------------

    if request.user.is_superuser:
        dioceses = Diocese.objects.filter(
            is_active=True
        ).order_by("name")

    elif profile and profile.role == "diocese_admin":
        dioceses = Diocese.objects.filter(
            id=profile.diocese_id,
            is_active=True,
        ).order_by("name")

    elif profile and profile.role == "parish_admin":
        if profile.parish_id:
            dioceses = Diocese.objects.filter(
                id=profile.parish.deanery.diocese_id,
                is_active=True,
            ).order_by("name")
        else:
            dioceses = Diocese.objects.none()

    elif profile and profile.role == "scc_leader":
        if profile.small_christian_community_id:
            dioceses = Diocese.objects.filter(
                id=profile.small_christian_community.zone.parish.deanery.diocese_id,
                is_active=True,
            ).order_by("name")
        else:
            dioceses = Diocese.objects.none()

    else:
        dioceses = Diocese.objects.none()


    # ---------------------------------------------------------
    # Deanery filter
    # ---------------------------------------------------------

    deaneries = Deanery.objects.none()

    if diocese_id:
        deaneries = Deanery.objects.filter(
            diocese_id=diocese_id,
            is_active=True,
        ).order_by("name")


    # ---------------------------------------------------------
    # Parish filter
    # ---------------------------------------------------------

    parishes = Parish.objects.none()

    if deanery_id:
        parishes = Parish.objects.filter(
            deanery_id=deanery_id,
            is_active=True,
        ).order_by("name")


    # ---------------------------------------------------------
    # Zone filter
    # ---------------------------------------------------------

    zones = Zone.objects.none()

    if parish_id:
        zones = Zone.objects.filter(
            parish_id=parish_id,
            is_active=True,
        ).order_by("name")


    # ---------------------------------------------------------
    # Small Christian Community filter
    # ---------------------------------------------------------

    small_christian_communities = SmallChristianCommunity.objects.none()

    if zone_id:
        small_christian_communities = SmallChristianCommunity.objects.filter(
            zone_id=zone_id,
            is_active=True,
        ).order_by("name")

    # Family names are derived from ChurchMember because
    # ChurchMember.family is currently a CharField.
    families = (
        family_members
        .exclude(family="")
        .values_list("family", flat=True)
        .distinct()
        .order_by("family")
    )

    context = {
        "members": members,
        "query": query,

        # Selected filters
        "selected_diocese": diocese_id,
        "selected_deanery": deanery_id,
        "selected_parish": parish_id,
        "selected_zone": zone_id,
        "selected_scc": scc_id,
        "selected_family": family_name,

        # Filter options
        "dioceses": dioceses,
        "deaneries": deaneries,
        "parishes": parishes,
        "zones": zones,
        "small_christian_communities": small_christian_communities,
        "families": families,
    }

    return render(
        request,
        "members/member_list.html",
        context,
    )

@login_required
@never_cache
def member_detail(request, pk):

    member = get_object_or_404(
        ChurchMember.objects
        .select_related(
            "small_christian_community__zone__parish__deanery__diocese"
        )
        .prefetch_related(
            "church_associations",
            "leadership_positions",
        ),
        pk=pk,
    )

    if not can_access_member(request.user, member):
        raise PermissionDenied

    context = {
        "member": member,
    }

    return render(
        request,
        "members/member_detail.html",
        context,
    )

@login_required
@never_cache
def member_update(request, pk):
    member = get_object_or_404(ChurchMember, pk=pk)

    if not can_access_member(request.user, member):
        raise PermissionDenied

    if request.method == "POST":
        form = ChurchMemberForm(request.POST, instance=member)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Church member information updated successfully."
            )
            return redirect("members:member_detail", pk=member.pk)
    else:
        form = ChurchMemberForm(instance=member)

    context = {
        "form": form,
        "member": member,
    }

    return render(request, "members/member_form.html", context)


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

    member = get_object_or_404(ChurchMember, pk=pk)

    if not can_access_member(request.user, member):
        raise PermissionDenied

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

    member = get_object_or_404(ChurchMember, pk=pk)

    if not can_access_member(request.user, member):
        raise PermissionDenied

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