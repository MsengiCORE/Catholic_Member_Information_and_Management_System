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
    get_user_profile,
    is_church_member,
    can_access_diocese,
    can_access_deanery,
    can_access_parish,
    can_access_zone,
    can_access_scc,
    can_access_family,
)

from .forms import (
    DioceseForm,
    DeaneryForm,
    ParishForm,
    ZoneForm,
    SmallChristianCommunityForm,
    FamilyForm,
    ChurchAssociationForm,
    ChurchMemberForm,
    MemberAssociationForm,
    LeadershipPositionForm,
    MemberLeadershipForm,
)

from accounts.models import UserProfile

from .models import (
    Diocese,
    Deanery,
    Parish,
    Zone,
    SmallChristianCommunity,
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

# =========================================================
# DIOCESE MANAGEMENT
# =========================================================

@login_required
@never_cache
def diocese_list(request):

    if request.user.is_superuser:

        dioceses = Diocese.objects.all().order_by("name")

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":
            dioceses = Diocese.objects.filter(
                id=profile.diocese_id
            ).order_by("name")

        elif profile.role == "parish_admin":
            if profile.parish_id:
                dioceses = Diocese.objects.filter(
                    id=profile.parish.deanery.diocese_id
                ).order_by("name")
            else:
                raise PermissionDenied

        elif profile.role == "scc_leader":
            if profile.small_christian_community_id:
                dioceses = Diocese.objects.filter(
                    id=(
                        profile
                        .small_christian_community
                        .zone
                        .parish
                        .deanery
                        .diocese_id
                    )
                ).order_by("name")
            else:
                raise PermissionDenied

        else:
            raise PermissionDenied

    context = {
        "dioceses": dioceses,
    }

    return render(
        request,
        "members/organization/dioceses/list.html",
        context,
    )

@login_required
@never_cache
def diocese_data(request):
    """
    Server-side DataTables endpoint for Dioceses.
    """

    if request.user.is_superuser:

        queryset = Diocese.objects.all()

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == UserProfile.Role.DIOCESE_ADMIN:

            queryset = Diocese.objects.filter(
                id=profile.diocese_id
            )

        elif profile.role == UserProfile.Role.PARISH_ADMIN:

            queryset = Diocese.objects.filter(
                id=profile.parish.deanery.diocese_id
            )

        elif profile.role == UserProfile.Role.SCC_LEADER:

            queryset = Diocese.objects.filter(
                id=profile.small_christian_community
                .zone.parish.deanery.diocese_id
            )

        else:
            raise PermissionDenied

    # -------------------------------------------------
    # DataTables parameters
    # -------------------------------------------------

    draw = int(request.GET.get("draw", 1))

    start = int(request.GET.get("start", 0))

    length = int(request.GET.get("length", 10))

    search_value = request.GET.get(
        "search[value]",
        ""
    ).strip()

    # -------------------------------------------------
    # Total records
    # -------------------------------------------------

    records_total = queryset.count()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    if search_value:

        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(description__icontains=search_value)
        )

    records_filtered = queryset.count()

    # -------------------------------------------------
    # Ordering
    # -------------------------------------------------

    order_column = request.GET.get(
        "order[0][column]",
        "1"
    )

    order_direction = request.GET.get(
        "order[0][dir]",
        "asc"
    )

    columns = {
        "0": "name",
        "1": "name",
        "2": "description",
        "3": "is_active",
    }

    order_field = columns.get(
        order_column,
        "name"
    )

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    # -------------------------------------------------
    # Pagination
    # -------------------------------------------------

    queryset = queryset[start:start + length]

    # -------------------------------------------------
    # Build response
    # -------------------------------------------------

    data = []

    for diocese in queryset:

        data.append({
            "id": str(diocese.pk),

            "name": diocese.name,

            "description": (
                diocese.description
                if diocese.description
                else "—"
            ),

            "status": (
                "Active"
                if diocese.is_active
                else "Inactive"
            ),

            "toggle_url": (
                f"/members/dioceses/"
                f"{diocese.pk}/toggle-status/"
            ),

            "is_active": diocese.is_active,
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })

@login_required
@never_cache
def diocese_create(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        form = DioceseForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Diocese created successfully."
            )

            return redirect(
                "members:diocese_list"
            )

    else:
        form = DioceseForm()

    context = {
        "form": form,
        "page_title": "Add Diocese",
        "submit_label": "Create Diocese",
    }

    return render(
        request,
        "members/organization/dioceses/form.html",
        context,
    )


@login_required
@never_cache
def diocese_update(request, pk):

    diocese = get_object_or_404(
        Diocese,
        pk=pk,
    )

    # Superuser can edit any Diocese.
    # Diocese Administrator can edit only their assigned Diocese.
    if not request.user.is_superuser:

        if request.user.profile.role != "diocese_admin":
            raise PermissionDenied

        if request.user.profile.diocese_id != diocese.id:
            raise PermissionDenied

    if request.method == "POST":

        form = DioceseForm(
            request.POST,
            instance=diocese,
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Diocese updated successfully."
            )

            return redirect(
                "members:diocese_list"
            )

    else:

        form = DioceseForm(
            instance=diocese,
        )

    context = {
        "form": form,
        "diocese": diocese,
        "page_title": "Edit Diocese",
        "submit_label": "Save Changes",
    }

    return render(
        request,
        "members/organization/dioceses/form.html",
        context,
    )


@login_required
@never_cache
def diocese_toggle_status(request, pk):

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method != "POST":
        raise PermissionDenied

    diocese = get_object_or_404(
        Diocese,
        pk=pk,
    )

    diocese.is_active = not diocese.is_active
    diocese.save(update_fields=["is_active", "updated_at"])

    if diocese.is_active:
        messages.success(
            request,
            f"{diocese.name} has been activated."
        )
    else:
        messages.warning(
            request,
            f"{diocese.name} has been deactivated."
        )

    return redirect(
        "members:diocese_list"
    )

# =========================================================
# DEANERY MANAGEMENT
# =========================================================

@login_required
@never_cache
def deanery_list(request):

    if request.user.is_superuser:

        deaneries = (
            Deanery.objects
            .select_related("diocese")
            .all()
            .order_by(
                "diocese__name",
                "name",
            )
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            deaneries = (
                Deanery.objects
                .select_related("diocese")
                .filter(
                    diocese_id=profile.diocese_id
                )
                .order_by("name")
            )

        elif profile.role == "parish_admin":

            deaneries = (
                Deanery.objects
                .select_related("diocese")
                .filter(
                    id=profile.parish.deanery_id
                )
                .order_by("name")
            )

        elif profile.role == "scc_leader":

            deaneries = (
                Deanery.objects
                .select_related("diocese")
                .filter(
                    id=(
                        profile
                        .small_christian_community
                        .zone
                        .parish
                        .deanery_id
                    )
                )
                .order_by("name")
            )

        else:
            raise PermissionDenied

    context = {
        "deaneries": deaneries,
    }

    return render(
        request,
        "members/organization/deaneries/list.html",
        context,
    )


@login_required
@never_cache
def deanery_data(request):
    """
    Server-side DataTables endpoint for Deaneries.
    """

    # ---------------------------------------------------------
    # ACCESS CONTROL
    # ---------------------------------------------------------
    if request.user.is_superuser:

        queryset = Deanery.objects.select_related(
            "diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            queryset = Deanery.objects.filter(
                diocese_id=profile.diocese_id
            ).select_related(
                "diocese"
            )

        elif profile.role == "parish_admin":

            queryset = Deanery.objects.filter(
                id=profile.parish.deanery_id
            ).select_related(
                "diocese"
            )

        elif profile.role == "scc_leader":

            queryset = Deanery.objects.filter(
                id=(
                    profile
                    .small_christian_community
                    .zone
                    .parish
                    .deanery_id
                )
            ).select_related(
                "diocese"
            )

        else:
            raise PermissionDenied

    # ---------------------------------------------------------
    # DATATABLES PARAMETERS
    # ---------------------------------------------------------
    draw = int(request.GET.get("draw", 1))
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))

    search_value = request.GET.get(
        "search[value]",
        ""
    ).strip()

    # ---------------------------------------------------------
    # TOTAL RECORDS
    # ---------------------------------------------------------
    records_total = queryset.count()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    if search_value:
        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(description__icontains=search_value)
            | Q(diocese__name__icontains=search_value)
        )

    records_filtered = queryset.count()

    # ---------------------------------------------------------
    # ORDERING
    # ---------------------------------------------------------
    order_column = request.GET.get(
        "order[0][column]",
        "1"
    )

    order_direction = request.GET.get(
        "order[0][dir]",
        "asc"
    )

    columns = {
        "0": "name",
        "1": "name",
        "2": "diocese__name",
        "3": "is_active",
    }

    order_field = columns.get(
        order_column,
        "name"
    )

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------
    queryset = queryset[start:start + length]

    # ---------------------------------------------------------
    # BUILD RESPONSE
    # ---------------------------------------------------------
    data = []

    for deanery in queryset:

        data.append({
            "id": str(deanery.pk),

            "name": deanery.name,

            "description": (
                deanery.description
                if deanery.description
                else "—"
            ),

            "diocese": deanery.diocese.name,

            "status": (
                "Active"
                if deanery.is_active
                else "Inactive"
            ),

            "is_active": deanery.is_active,

            "edit_url": (
                f"/members/deaneries/"
                f"{deanery.pk}/edit/"
            ),
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })

@login_required
@never_cache
@require_role("diocese_admin")
def deanery_create(request):

    if request.method == "POST":

        form = DeaneryForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            deanery = form.save()

            messages.success(
                request,
                f"Deanery '{deanery.name}' created successfully."
            )

            return redirect(
                "members:deanery_list"
            )

    else:

        form = DeaneryForm(
            user=request.user,
        )

    context = {
        "form": form,
        "page_title": "Add Deanery",
        "submit_label": "Create Deanery",
    }

    return render(
        request,
        "members/organization/deaneries/form.html",
        context,
    )


@login_required
@never_cache
@require_role("diocese_admin")
def deanery_update(request, pk):

    deanery = get_object_or_404(
        Deanery.objects.select_related("diocese"),
        pk=pk,
    )

    profile = None

    if request.user.is_superuser:

        queryset = Deanery.objects.select_related(
            "diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == UserProfile.Role.DIOCESE_ADMIN:

            queryset = Deanery.objects.filter(
                diocese_id=profile.diocese_id
            ).select_related(
                "diocese"
            )

        elif profile.role == UserProfile.Role.PARISH_ADMIN:

            queryset = Deanery.objects.filter(
                id=profile.parish.deanery_id
            ).select_related(
                "diocese"
            )

        elif profile.role == UserProfile.Role.SCC_LEADER:

            queryset = Deanery.objects.filter(
                id=profile.small_christian_community
                .zone.parish.deanery_id
            ).select_related(
                "diocese"
            )

        else:
            raise PermissionDenied

    if request.method == "POST":

        form = DeaneryForm(
            request.POST,
            instance=deanery,
            user=request.user,
        )

        if form.is_valid():

            # Extra server-side scope check.
            selected_diocese = form.cleaned_data["diocese"]

            if (
                not request.user.is_superuser
                and selected_diocese.id != profile.diocese_id
            ):
                raise PermissionDenied

            form.save()

            messages.success(
                request,
                f"Deanery '{deanery.name}' updated successfully."
            )

            return redirect(
                "members:deanery_list"
            )

    else:

        form = DeaneryForm(
            instance=deanery,
            user=request.user,
        )

    context = {
        "form": form,
        "deanery": deanery,
        "page_title": "Edit Deanery",
        "submit_label": "Save Changes",
    }

    return render(
        request,
        "members/organization/deaneries/form.html",
        context,
    )


@login_required
@never_cache
def parish_list(request):

    if request.user.is_superuser:

        parishes = Parish.objects.select_related(
            "deanery__diocese"
        ).order_by(
            "deanery__diocese__name",
            "deanery__name",
            "name",
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            parishes = Parish.objects.filter(
                deanery__diocese_id=profile.diocese_id
            ).select_related(
                "deanery__diocese"
            ).order_by(
                "deanery__name",
                "name",
            )

        elif profile.role == "parish_admin":

            parishes = Parish.objects.filter(
                id=profile.parish_id
            ).select_related(
                "deanery__diocese"
            )

        elif profile.role == "scc_leader":

            parishes = Parish.objects.filter(
                id=profile.small_christian_community
                .zone.parish_id
            ).select_related(
                "deanery__diocese"
            )

        else:
            raise PermissionDenied

    context = {
        "parishes": parishes,
    }

    return render(
        request,
        "members/organization/parishes/list.html",
        context,
    )


@login_required
@never_cache
def parish_data(request):
    """
    Server-side DataTables endpoint for Parishes.
    """

    # ---------------------------------------------------------
    # ACCESS CONTROL
    # ---------------------------------------------------------
    if request.user.is_superuser:

        queryset = Parish.objects.select_related(
            "deanery__diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            queryset = Parish.objects.filter(
                deanery__diocese_id=profile.diocese_id
            ).select_related(
                "deanery__diocese"
            )

        elif profile.role == "parish_admin":

            queryset = Parish.objects.filter(
                id=profile.parish_id
            ).select_related(
                "deanery__diocese"
            )

        elif profile.role == "scc_leader":

            queryset = Parish.objects.filter(
                id=profile.small_christian_community.zone.parish_id
            ).select_related(
                "deanery__diocese"
            )

        else:
            raise PermissionDenied

    # ---------------------------------------------------------
    # DATATABLES PARAMETERS
    # ---------------------------------------------------------
    draw = int(
        request.GET.get("draw", 1)
    )

    start = int(
        request.GET.get("start", 0)
    )

    length = int(
        request.GET.get("length", 10)
    )

    search_value = request.GET.get(
        "search[value]",
        ""
    ).strip()

    # ---------------------------------------------------------
    # TOTAL RECORDS
    # ---------------------------------------------------------
    records_total = queryset.count()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    if search_value:

        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(description__icontains=search_value)
            | Q(deanery__name__icontains=search_value)
            | Q(deanery__diocese__name__icontains=search_value)
        )

    records_filtered = queryset.count()

    # ---------------------------------------------------------
    # ORDERING
    # ---------------------------------------------------------
    order_column = request.GET.get(
        "order[0][column]",
        "1"
    )

    order_direction = request.GET.get(
        "order[0][dir]",
        "asc"
    )

    columns = {
        "0": "name",
        "1": "name",
        "2": "deanery__name",
        "3": "deanery__diocese__name",
        "4": "description",
        "5": "is_active",
    }

    order_field = columns.get(
        order_column,
        "name"
    )

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(
        order_field
    )

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------
    queryset = queryset[
        start:start + length
    ]

    # ---------------------------------------------------------
    # RESPONSE DATA
    # ---------------------------------------------------------
    data = []

    for parish in queryset:

        data.append({
            "id": str(parish.pk),

            "name": parish.name,

            "deanery": parish.deanery.name,

            "diocese": parish.deanery.diocese.name,

            "description": (
                parish.description
                if parish.description
                else "—"
            ),

            "status": (
                "Active"
                if parish.is_active
                else "Inactive"
            ),

            "is_active": parish.is_active,

            "edit_url": (
                f"/members/parishes/"
                f"{parish.pk}/edit/"
            ),
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })

@require_role("diocese_admin")
@login_required
@never_cache
def parish_create(request):
    """
    Create a Parish within the Diocese Administrator's scope.
    Superusers can create a Parish in any active Diocese.
    """

    if request.method == "POST":
        form = ParishForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():
            parish = form.save()

            messages.success(
                request,
                f'Parish "{parish.name}" was created successfully.'
            )

            return redirect("members:parish_list")

    else:
        form = ParishForm(
            user=request.user,
        )

    context = {
        "form": form,
        "title": "Add Parish",
        "submit_text": "Create Parish",
    }

    return render(
        request,
        "members/organization/parishes/form.html",
        context,
    )


@require_role("diocese_admin")
@login_required
@never_cache
def parish_update(request, pk):
    """
    Update a Parish within the user's organizational scope.
    """

    parish = get_object_or_404(
        Parish.objects.select_related(
            "deanery__diocese"
        ),
        pk=pk,
    )

    # Superuser can edit any Parish.
    if request.user.is_superuser:

        queryset = Parish.objects.select_related(
            "deanery__diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == UserProfile.Role.DIOCESE_ADMIN:

            queryset = Parish.objects.filter(
                deanery__diocese_id=profile.diocese_id
            ).select_related(
                "deanery__diocese"
            )

        elif profile.role == UserProfile.Role.PARISH_ADMIN:

            queryset = Parish.objects.filter(
                id=profile.parish_id
            ).select_related(
                "deanery__diocese"
            )

        elif profile.role == UserProfile.Role.SCC_LEADER:

            queryset = Parish.objects.filter(
                id=profile.small_christian_community.zone.parish_id
            ).select_related(
                "deanery__diocese"
            )

        else:
            raise PermissionDenied

    if request.method == "POST":

        form = ParishForm(
            request.POST,
            instance=parish,
            user=request.user,
        )

        if form.is_valid():
            parish = form.save()

            messages.success(
                request,
                f'Parish "{parish.name}" was updated successfully.'
            )

            return redirect("members:parish_list")

    else:

        form = ParishForm(
            instance=parish,
            user=request.user,
        )

    context = {
        "form": form,
        "parish": parish,
        "title": "Edit Parish",
        "submit_text": "Update Parish",
    }

    return render(
        request,
        "members/organization/parishes/form.html",
        context,
    )


@login_required
@never_cache
def zone_list(request):

    if request.user.is_superuser:

        zones = Zone.objects.select_related(
            "parish__deanery__diocese"
        ).order_by(
            "parish__deanery__diocese__name",
            "parish__deanery__name",
            "parish__name",
            "name",
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            zones = Zone.objects.filter(
                parish__deanery__diocese_id=profile.diocese_id
            ).select_related(
                "parish__deanery__diocese"
            ).order_by(
                "parish__deanery__name",
                "parish__name",
                "name",
            )

        elif profile.role == "parish_admin":

            zones = Zone.objects.filter(
                parish_id=profile.parish_id
            ).select_related(
                "parish__deanery__diocese"
            ).order_by("name")

        elif profile.role == "scc_leader":

            zones = Zone.objects.filter(
                id=profile.small_christian_community.zone_id
            ).select_related(
                "parish__deanery__diocese"
            ).order_by("name")

        else:
            raise PermissionDenied

    context = {
        "zones": zones,
    }

    return render(
        request,
        "members/organization/zones/list.html",
        context,
    )


@login_required
@never_cache
def zone_data(request):
    """
    Server-side DataTables endpoint for Zones.
    """

    # ---------------------------------------------------------
    # ACCESS CONTROL
    # ---------------------------------------------------------
    if request.user.is_superuser:

        queryset = Zone.objects.select_related(
            "parish__deanery__diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            queryset = Zone.objects.filter(
                parish__deanery__diocese_id=profile.diocese_id
            ).select_related(
                "parish__deanery__diocese"
            )

        elif profile.role == "parish_admin":

            queryset = Zone.objects.filter(
                parish_id=profile.parish_id
            ).select_related(
                "parish__deanery__diocese"
            )

        elif profile.role == "scc_leader":

            queryset = Zone.objects.filter(
                id=profile.small_christian_community.zone_id
            ).select_related(
                "parish__deanery__diocese"
            )

        else:
            raise PermissionDenied

    # ---------------------------------------------------------
    # DATATABLES PARAMETERS
    # ---------------------------------------------------------
    draw = int(
        request.GET.get("draw", 1)
    )

    start = int(
        request.GET.get("start", 0)
    )

    length = int(
        request.GET.get("length", 10)
    )

    search_value = request.GET.get(
        "search[value]",
        ""
    ).strip()

    # ---------------------------------------------------------
    # TOTAL RECORDS
    # ---------------------------------------------------------
    records_total = queryset.count()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    if search_value:

        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(parish__name__icontains=search_value)
            | Q(parish__deanery__name__icontains=search_value)
            | Q(
                parish__deanery__diocese__name__icontains=search_value
            )
        )

    records_filtered = queryset.count()

    # ---------------------------------------------------------
    # ORDERING
    # ---------------------------------------------------------
    order_column = request.GET.get(
        "order[0][column]",
        "1"
    )

    order_direction = request.GET.get(
        "order[0][dir]",
        "asc"
    )

    columns = {
        "0": "name",
        "1": "name",
        "2": "parish__name",
        "3": "parish__deanery__name",
        "4": "parish__deanery__diocese__name",
        "5": "is_active",
    }

    order_field = columns.get(
        order_column,
        "name"
    )

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(
        order_field
    )

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------
    queryset = queryset[
        start:start + length
    ]

    # ---------------------------------------------------------
    # RESPONSE DATA
    # ---------------------------------------------------------
    data = []

    for zone in queryset:

        data.append({
            "id": str(zone.pk),

            "name": zone.name,

            "parish": zone.parish.name,

            "deanery": zone.parish.deanery.name,

            "diocese": zone.parish.deanery.diocese.name,

            "status": (
                "Active"
                if zone.is_active
                else "Inactive"
            ),

            "is_active": zone.is_active,

            "edit_url": (
                f"/members/zones/"
                f"{zone.pk}/edit/"
            ),
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })

@require_role("diocese_admin")
@login_required
@never_cache
def zone_create(request):
    """
    Create a Zone within the user's organizational scope.
    """

    if request.method == "POST":

        form = ZoneForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            zone = form.save()

            messages.success(
                request,
                f'Zone "{zone.name}" was created successfully.'
            )

            return redirect("members:zone_list")

    else:

        form = ZoneForm(
            user=request.user,
        )

    context = {
        "form": form,
        "title": "Add Zone",
        "submit_text": "Create Zone",
    }

    return render(
        request,
        "members/organization/zones/form.html",
        context,
    )


@require_role("diocese_admin")
@login_required
@never_cache
def zone_update(request, pk):
    """
    Update a Zone within the user's organizational scope.
    """

    zone = get_object_or_404(
        Zone.objects.select_related(
            "parish__deanery__diocese"
        ),
        pk=pk,
    )

    # Superuser can edit any Zone.
    if not request.user.is_superuser:

        profile = get_user_profile(request.user)

        if (
            profile is None
            or profile.role != "diocese_admin"
            or profile.diocese_id is None
        ):
            raise PermissionDenied

        # Zone must belong to the administrator's Diocese.
        if zone.parish.deanery.diocese_id != profile.diocese_id:
            raise PermissionDenied

    if request.method == "POST":

        form = ZoneForm(
            request.POST,
            instance=zone,
            user=request.user,
        )

        if form.is_valid():

            zone = form.save()

            messages.success(
                request,
                f'Zone "{zone.name}" was updated successfully.'
            )

            return redirect("members:zone_list")

    else:

        form = ZoneForm(
            instance=zone,
            user=request.user,
        )

    context = {
        "form": form,
        "zone": zone,
        "title": "Edit Zone",
        "submit_text": "Update Zone",
    }

    return render(
        request,
        "members/organization/zones/form.html",
        context,
    )


@login_required
@never_cache
def small_christian_community_list(request):

    if not request.user.is_superuser:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role not in (
            "diocese_admin",
            "parish_admin",
            "scc_leader",
        ):
            raise PermissionDenied

    return render(
        request,
        "members/organization/small_christian_communities/list.html",
    )


@login_required
@never_cache
def small_christian_community_data(request):

    if request.user.is_superuser:

        queryset = SmallChristianCommunity.objects.select_related(
            "zone__parish__deanery__diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            queryset = SmallChristianCommunity.objects.filter(
                zone__parish__deanery__diocese_id=profile.diocese_id
            ).select_related(
                "zone__parish__deanery__diocese"
            )

        elif profile.role == "parish_admin":

            queryset = SmallChristianCommunity.objects.filter(
                zone__parish_id=profile.parish_id
            ).select_related(
                "zone__parish__deanery__diocese"
            )

        elif profile.role == "scc_leader":

            queryset = SmallChristianCommunity.objects.filter(
                id=profile.small_christian_community_id
            ).select_related(
                "zone__parish__deanery__diocese"
            )

        else:
            raise PermissionDenied

    # -------------------------------------------------
    # DataTables parameters
    # -------------------------------------------------

    draw = int(request.GET.get("draw", 1))

    start = int(request.GET.get("start", 0))

    length = int(request.GET.get("length", 10))

    search_value = request.GET.get(
        "search[value]",
        ""
    ).strip()

    # -------------------------------------------------
    # Total records before filtering
    # -------------------------------------------------

    records_total = queryset.count()

    # -------------------------------------------------
    # Search
    # -------------------------------------------------

    if search_value:

        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(zone__name__icontains=search_value)
            | Q(zone__parish__name__icontains=search_value)
            | Q(zone__parish__deanery__name__icontains=search_value)
            | Q(
                zone__parish__deanery__diocese__name__icontains=
                search_value
            )
        )

    records_filtered = queryset.count()

    # -------------------------------------------------
    # Ordering
    # -------------------------------------------------

    order_column = request.GET.get(
        "order[0][column]",
        "1"
    )

    order_direction = request.GET.get(
        "order[0][dir]",
        "asc"
    )

    columns = {
        "0": "name",
        "1": "name",
        "2": "zone__name",
        "3": "zone__parish__name",
        "4": "zone__parish__deanery__name",
        "5": "zone__parish__deanery__diocese__name",
        "6": "is_active",
    }

    order_field = columns.get(
        order_column,
        "name"
    )

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(order_field)

    # -------------------------------------------------
    # Pagination
    # -------------------------------------------------

    queryset = queryset[start:start + length]

    # -------------------------------------------------
    # Build response
    # -------------------------------------------------

    data = []

    for community in queryset:

        data.append({
            "name": community.name,

            "zone": community.zone.name,

            "parish": community.zone.parish.name,

            "deanery": (
                community
                .zone
                .parish
                .deanery
                .name
            ),

            "diocese": (
                community
                .zone
                .parish
                .deanery
                .diocese
                .name
            ),

            "status": (
                "Active"
                if community.is_active
                else "Inactive"
            ),

            "actions": (
                f'<a href="/members/'
                f'small-christian-communities/'
                f'{community.pk}/edit/" '
                f'class="btn btn-sm btn-outline">'
                f'Edit'
                f'</a>'
            ),
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })

@require_role("diocese_admin")
@login_required
@never_cache
def small_christian_community_create(request):
    """
    Create a Small Christian Community within the
    user's organizational scope.
    """

    if request.method == "POST":

        form = SmallChristianCommunityForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            community = form.save()

            messages.success(
                request,
                f'Small Christian Community "{community.name}" '
                f'was created successfully.'
            )

            return redirect(
                "members:small_christian_community_list"
            )

    else:

        form = SmallChristianCommunityForm(
            user=request.user,
        )

    context = {
        "form": form,
        "title": "Add Small Christian Community",
        "submit_text": "Create SCC",
    }

    return render(
        request,
        "members/organization/small_christian_communities/form.html",
        context,
    )


@require_role("diocese_admin")
@login_required
@never_cache
def small_christian_community_update(request, pk):
    """
    Update a Small Christian Community within the
    user's organizational scope.
    """

    community = get_object_or_404(
        SmallChristianCommunity.objects.select_related(
            "zone__parish__deanery__diocese"
        ),
        pk=pk,
    )

    # Superuser can edit any SCC.
    if not request.user.is_superuser:

        profile = get_user_profile(request.user)

        if (
            profile is None
            or profile.role != "diocese_admin"
            or profile.diocese_id is None
        ):
            raise PermissionDenied

        # SCC must belong to the administrator's Diocese.
        if (
            community.zone.parish.deanery.diocese_id
            != profile.diocese_id
        ):
            raise PermissionDenied

    if request.method == "POST":

        form = SmallChristianCommunityForm(
            request.POST,
            instance=community,
            user=request.user,
        )

        if form.is_valid():

            community = form.save()

            messages.success(
                request,
                f'Small Christian Community "{community.name}" '
                f'was updated successfully.'
            )

            return redirect(
                "members:small_christian_community_list"
            )

    else:

        form = SmallChristianCommunityForm(
            instance=community,
            user=request.user,
        )

    context = {
        "form": form,
        "community": community,
        "title": "Edit Small Christian Community",
        "submit_text": "Update SCC",
    }

    return render(
        request,
        "members/organization/small_christian_communities/form.html",
        context,
    )


@login_required
@never_cache
def family_list(request):

    if request.user.is_superuser:

        families = Family.objects.select_related(
            "small_christian_community__zone__parish__deanery__diocese"
        ).order_by(
            "small_christian_community__zone__parish__deanery__diocese__name",
            "small_christian_community__zone__parish__deanery__name",
            "small_christian_community__zone__parish__name",
            "small_christian_community__zone__name",
            "small_christian_community__name",
            "name",
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            families = Family.objects.filter(
                small_christian_community__zone__parish__deanery__diocese_id=
                profile.diocese_id
            ).select_related(
                "small_christian_community__zone__parish__deanery__diocese"
            )

        elif profile.role == "parish_admin":

            families = Family.objects.filter(
                small_christian_community__zone__parish_id=
                profile.parish_id
            ).select_related(
                "small_christian_community__zone__parish__deanery__diocese"
            )

        elif profile.role == "scc_leader":

            families = Family.objects.filter(
                small_christian_community_id=
                profile.small_christian_community_id
            ).select_related(
                "small_christian_community__zone__parish__deanery__diocese"
            )

        else:
            raise PermissionDenied

    context = {
        "families": families,
    }

    return render(
        request,
        "members/organization/families/list.html",
        context,
    )


@login_required
@never_cache
def family_data(request):
    """
    Server-side DataTables endpoint for Families.
    """

    # ---------------------------------------------------------
    # ACCESS CONTROL
    # ---------------------------------------------------------
    if request.user.is_superuser:

        queryset = Family.objects.select_related(
            "small_christian_community__zone__parish__deanery__diocese"
        )

    else:

        profile = get_user_profile(request.user)

        if profile is None:
            raise PermissionDenied

        if profile.role == "diocese_admin":

            queryset = Family.objects.filter(
                small_christian_community__zone__parish__deanery__diocese_id=
                profile.diocese_id
            ).select_related(
                "small_christian_community__zone__parish__deanery__diocese"
            )

        elif profile.role == "parish_admin":

            queryset = Family.objects.filter(
                small_christian_community__zone__parish_id=
                profile.parish_id
            ).select_related(
                "small_christian_community__zone__parish__deanery__diocese"
            )

        elif profile.role == "scc_leader":

            queryset = Family.objects.filter(
                small_christian_community_id=
                profile.small_christian_community_id
            ).select_related(
                "small_christian_community__zone__parish__deanery__diocese"
            )

        else:
            raise PermissionDenied

    # ---------------------------------------------------------
    # DATATABLES PARAMETERS
    # ---------------------------------------------------------
    draw = int(
        request.GET.get("draw", 1)
    )

    start = int(
        request.GET.get("start", 0)
    )

    length = int(
        request.GET.get("length", 10)
    )

    search_value = request.GET.get(
        "search[value]",
        ""
    ).strip()

    # ---------------------------------------------------------
    # TOTAL RECORDS
    # ---------------------------------------------------------
    records_total = queryset.count()

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------
    if search_value:

        queryset = queryset.filter(
            Q(name__icontains=search_value)
            | Q(
                small_christian_community__name__icontains=search_value
            )
            | Q(
                small_christian_community__zone__name__icontains=search_value
            )
            | Q(
                small_christian_community__zone__parish__name__icontains=search_value
            )
            | Q(
                small_christian_community__zone__parish__deanery__name__icontains=search_value
            )
            | Q(
                small_christian_community__zone__parish__deanery__diocese__name__icontains=search_value
            )
        )

    records_filtered = queryset.count()

    # ---------------------------------------------------------
    # ORDERING
    # ---------------------------------------------------------
    order_column = request.GET.get(
        "order[0][column]",
        "1"
    )

    order_direction = request.GET.get(
        "order[0][dir]",
        "asc"
    )

    columns = {
        "0": "name",
        "1": "name",
        "2": "small_christian_community__name",
        "3": "small_christian_community__zone__name",
        "4": "small_christian_community__zone__parish__name",
        "5": "small_christian_community__zone__parish__deanery__name",
        "6": "small_christian_community__zone__parish__deanery__diocese__name",
        "7": "is_active",
    }

    order_field = columns.get(
        order_column,
        "name"
    )

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(
        order_field
    )

    # ---------------------------------------------------------
    # PAGINATION
    # ---------------------------------------------------------
    queryset = queryset[
        start:start + length
    ]

    # ---------------------------------------------------------
    # RESPONSE DATA
    # ---------------------------------------------------------
    data = []

    for family in queryset:

        scc = family.small_christian_community
        zone = scc.zone
        parish = zone.parish
        deanery = parish.deanery
        diocese = deanery.diocese

        data.append({
            "id": str(family.pk),

            "name": family.name,

            "scc": scc.name,

            "zone": zone.name,

            "parish": parish.name,

            "deanery": deanery.name,

            "diocese": diocese.name,

            "status": (
                "Active"
                if family.is_active
                else "Inactive"
            ),

            "is_active": family.is_active,

            "edit_url": (
                f"/members/families/"
                f"{family.pk}/edit/"
            ),
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })

@require_role("diocese_admin")
@login_required
@never_cache
def family_create(request):
    """
    Create a Family within the user's organizational scope.
    """

    if request.method == "POST":

        form = FamilyForm(
            request.POST,
            user=request.user,
        )

        if form.is_valid():

            family = form.save()

            messages.success(
                request,
                f'Family "{family.name}" was created successfully.'
            )

            return redirect("members:family_list")

    else:

        form = FamilyForm(
            user=request.user,
        )

    context = {
        "form": form,
        "title": "Add Family",
        "submit_text": "Create Family",
    }

    return render(
        request,
        "members/organization/families/form.html",
        context,
    )


@require_role("diocese_admin")
@login_required
@never_cache
def family_update(request, pk):
    """
    Update a Family within the user's organizational scope.
    """

    family = get_object_or_404(
        Family.objects.select_related(
            "small_christian_community__zone__parish__deanery__diocese"
        ),
        pk=pk,
    )

    # Superuser can edit any Family.
    if not request.user.is_superuser:

        profile = get_user_profile(request.user)

        if (
            profile is None
            or profile.role != "diocese_admin"
            or profile.diocese_id is None
        ):
            raise PermissionDenied

        # Family must belong to the administrator's Diocese.
        if (
            family
            .small_christian_community
            .zone
            .parish
            .deanery
            .diocese_id
            != profile.diocese_id
        ):
            raise PermissionDenied

    if request.method == "POST":

        form = FamilyForm(
            request.POST,
            instance=family,
            user=request.user,
        )

        if form.is_valid():

            family = form.save()

            messages.success(
                request,
                f'Family "{family.name}" was updated successfully.'
            )

            return redirect("members:family_list")

    else:

        form = FamilyForm(
            instance=family,
            user=request.user,
        )

    context = {
        "form": form,
        "family": family,
        "title": "Edit Family",
        "submit_text": "Update Family",
    }

    return render(
        request,
        "members/organization/families/form.html",
        context,
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
    """
    Member list page.

    IMPORTANT:
    The actual member records are loaded by DataTables through the
    server-side `member_data` endpoint. This view only prepares the
    relatively small organizational filter options and therefore does
    not evaluate the full ChurchMember queryset during page rendering.
    """
    if not can_manage_members(request.user) and not is_church_member(request.user):
        raise PermissionDenied

    # Selected filters are retained by the page so that DataTables can
    # send them to the server-side endpoint.
    query = request.GET.get("q", "").strip()

    diocese_id = request.GET.get("diocese", "").strip()
    deanery_id = request.GET.get("deanery", "").strip()
    parish_id = request.GET.get("parish", "").strip()
    zone_id = request.GET.get("zone", "").strip()
    scc_id = request.GET.get("scc", "").strip()
    family_name = request.GET.get("family", "").strip()

    profile = None

    if not request.user.is_superuser:
        profile = get_user_profile(request.user)

    # ---------------------------------------------------------
    # Diocese filter options
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
    # Cascading organizational filter options
    # ---------------------------------------------------------
    deaneries = Deanery.objects.none()
    if diocese_id:
        deaneries = Deanery.objects.filter(
            diocese_id=diocese_id,
            is_active=True,
        ).order_by("name")

    parishes = Parish.objects.none()
    if deanery_id:
        parishes = Parish.objects.filter(
            deanery_id=deanery_id,
            is_active=True,
        ).order_by("name")

    zones = Zone.objects.none()
    if parish_id:
        zones = Zone.objects.filter(
            parish_id=parish_id,
            is_active=True,
        ).order_by("name")

    small_christian_communities = SmallChristianCommunity.objects.none()
    if zone_id:
        small_christian_communities = SmallChristianCommunity.objects.filter(
            zone_id=zone_id,
            is_active=True,
        ).order_by("name")

    # ---------------------------------------------------------
    # Family options
    #
    # ChurchMember.family is intentionally a CharField.
    # Only fetch family names for the user's accessible scope.
    # ---------------------------------------------------------
    family_members = get_accessible_members(
        request.user,
        ChurchMember.objects.all(),
    )

    if scc_id:
        family_members = family_members.filter(
            small_christian_community_id=scc_id
        )
    elif zone_id:
        family_members = family_members.filter(
            small_christian_community__zone_id=zone_id
        )
    elif parish_id:
        family_members = family_members.filter(
            small_christian_community__zone__parish_id=parish_id
        )
    elif deanery_id:
        family_members = family_members.filter(
            small_christian_community__zone__parish__deanery_id=deanery_id
        )
    elif diocese_id:
        family_members = family_members.filter(
            small_christian_community__zone__parish__deanery__diocese_id=diocese_id
        )

    families = (
        family_members
        .exclude(family="")
        .values_list("family", flat=True)
        .distinct()
        .order_by("family")
    )

    context = {
        # No "members" queryset is intentionally passed here.
        # DataTables obtains members through member_data.
        "query": query,

        "selected_diocese": diocese_id,
        "selected_deanery": deanery_id,
        "selected_parish": parish_id,
        "selected_zone": zone_id,
        "selected_scc": scc_id,
        "selected_family": family_name,

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
def member_data(request):
    """
    Server-side DataTables endpoint for Church Members.

    Only the requested DataTables page is fetched from PostgreSQL.
    Search, organizational filters, ordering and pagination are all
    performed at database level.
    """
    if not can_manage_members(request.user) and not is_church_member(request.user):
        raise PermissionDenied

    # ---------------------------------------------------------
    # Base queryset + organizational access scope
    # ---------------------------------------------------------
    queryset = ChurchMember.objects.select_related(
        "small_christian_community__zone__parish__deanery__diocese"
    )

    queryset = get_accessible_members(
        request.user,
        queryset,
    )

    # ---------------------------------------------------------
    # Custom filters from the member list page
    # ---------------------------------------------------------
    query = request.GET.get("q", "").strip()
    diocese_id = request.GET.get("diocese", "").strip()
    deanery_id = request.GET.get("deanery", "").strip()
    parish_id = request.GET.get("parish", "").strip()
    zone_id = request.GET.get("zone", "").strip()
    scc_id = request.GET.get("scc", "").strip()
    family_name = request.GET.get("family", "").strip()

    if query:
        queryset = queryset.filter(
            Q(digital_offering_number__icontains=query)
            | Q(first_name__icontains=query)
            | Q(middle_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(email__icontains=query)
        )

    if diocese_id:
        queryset = queryset.filter(
            small_christian_community__zone__parish__deanery__diocese_id=diocese_id
        )

    if deanery_id:
        queryset = queryset.filter(
            small_christian_community__zone__parish__deanery_id=deanery_id
        )

    if parish_id:
        queryset = queryset.filter(
            small_christian_community__zone__parish_id=parish_id
        )

    if zone_id:
        queryset = queryset.filter(
            small_christian_community__zone_id=zone_id
        )

    if scc_id:
        queryset = queryset.filter(
            small_christian_community_id=scc_id
        )

    if family_name:
        queryset = queryset.filter(
            family__iexact=family_name
        )

    # ---------------------------------------------------------
    # DataTables parameters
    # ---------------------------------------------------------
    try:
        draw = int(request.GET.get("draw", 1))
    except (TypeError, ValueError):
        draw = 1

    try:
        start = max(int(request.GET.get("start", 0)), 0)
    except (TypeError, ValueError):
        start = 0

    try:
        length = int(request.GET.get("length", 10))
    except (TypeError, ValueError):
        length = 10

    # Protect the endpoint from accidentally requesting an enormous page.
    if length < 1:
        length = 10
    length = min(length, 100)

    # DataTables sends its own search[value]. The custom q field is also
    # supported so the existing search box remains the source of truth.
    dt_search = request.GET.get("search[value]", "").strip()

    if dt_search and not query:
        queryset = queryset.filter(
            Q(digital_offering_number__icontains=dt_search)
            | Q(first_name__icontains=dt_search)
            | Q(middle_name__icontains=dt_search)
            | Q(last_name__icontains=dt_search)
            | Q(phone_number__icontains=dt_search)
            | Q(email__icontains=dt_search)
        )

    # ---------------------------------------------------------
    # Counts
    # ---------------------------------------------------------
    records_total = get_accessible_members(
        request.user,
        ChurchMember.objects.all(),
    ).count()

    records_filtered = queryset.count()

    # ---------------------------------------------------------
    # Ordering
    # ---------------------------------------------------------
    order_column = request.GET.get("order[0][column]", "2")
    order_direction = request.GET.get("order[0][dir]", "asc")

    columns = {
        "0": "last_name",
        "1": "digital_offering_number",
        "2": "last_name",
        "3": "phone_number",
        "4": "email",
        "5": "marital_status",
        "6": "baptism_status",
    }

    order_field = columns.get(order_column, "last_name")

    if order_direction == "desc":
        order_field = f"-{order_field}"

    queryset = queryset.order_by(
        order_field,
        "first_name",
        "middle_name",
        "pk",
    )

    # ---------------------------------------------------------
    # Database pagination
    # ---------------------------------------------------------
    page_queryset = queryset[start:start + length]

    # ---------------------------------------------------------
    # Response
    # ---------------------------------------------------------
    data = []

    for member in page_queryset:
        full_name = " ".join(
            part
            for part in (
                member.first_name,
                member.middle_name,
                member.last_name,
            )
            if part
        )

        data.append({
            "id": str(member.pk),
            "digital_offering_number": member.digital_offering_number,
            "full_name": full_name,
            "phone": member.phone_number or "—",
            "email": member.email or "—",
            "marital_status": member.get_marital_status_display(),
            "baptism_status": member.get_baptism_status_display(),
            "detail_url": f"/members/member-details/{member.pk}/",
        })

    return JsonResponse({
        "draw": draw,
        "recordsTotal": records_total,
        "recordsFiltered": records_filtered,
        "data": data,
    })


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