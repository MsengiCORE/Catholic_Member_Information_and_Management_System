from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse

from .forms import (
    MarriageRequestForm,
    TransferRequestForm,
    TravelCertificateRequestForm,
)
from .models import (
    MarriageRequest,
    TransferRequest,
    TravelCertificateRequest,
)
from members.models import ChurchMember, SmallChristianCommunity
from .permissions import (
    can_approve_travel_certificate_requests,
    can_review_marriage_requests,
    can_review_transfer_requests,
    can_submit_marriage_request,
    can_submit_transfer_request,
    can_submit_travel_certificate_request,
    can_view_marriage_requests,
    can_view_travel_certificate_requests,
    can_view_transfer_requests,
    can_access_request,
    can_access_transfer_request,
    get_user_church_member,
)


# ============================================================
# Helpers
# ============================================================

def _get_member_or_denied(user):
    """
    Return the ChurchMember belonging to the authenticated user.

    A user who does not have an associated ChurchMember cannot
    submit member requests.
    """
    member = get_user_church_member(user)

    if not member:
        raise PermissionDenied(
            "Your account is not linked to a Church Member."
        )

    return member


def _can_view_member_request(user, request_object):
    """
    Check whether the authenticated user can view a request.

    Access is granted when:
    - the user has the appropriate view permission, and
    - the request belongs to the user, or
    - the user has organizational scope over the member.
    """
    return can_access_request(user, request_object)


def _ensure_status(request_object, allowed_statuses):
    """
    Validate that a request is currently in one of the allowed
    statuses before performing a workflow action.
    """
    if request_object.status not in allowed_statuses:
        raise PermissionDenied(
            "This request cannot be processed in its current status."
        )


# ============================================================
# MARRIAGE REQUESTS
# ============================================================

@never_cache
@login_required(login_url="accounts:login")
def marriage_request_list(request):
    """
    Display marriage requests accessible to the current user.
    """

    if not can_view_marriage_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to view marriage requests."
        )

    queryset = (
        MarriageRequest.objects
        .select_related(
            "church_member",
            "applicant",
            "reviewed_by",
        )
        .order_by("-submitted_at")
    )

    # Superuser can see everything.
    if request.user.is_superuser:
        pass

    # Applicant sees own requests.
    elif request.user.church_member if hasattr(
        request.user,
        "church_member",
    ) else False:
        queryset = queryset.filter(
            applicant=request.user
        )

    else:
        # Organizational users need scope filtering.
        queryset = queryset.filter(
            church_member__in=get_user_accessible_members(
                request.user
            )
        )

    return render(
        request,
        "member_requests/marriage/list.html",
        {
            "marriage_requests": queryset,
        },
    )


@never_cache
@login_required(login_url="accounts:login")
def marriage_request_create(request):
    """
    Submit a new marriage request.
    """

    if not can_submit_marriage_request(request.user):
        raise PermissionDenied(
            "You do not have permission to submit marriage requests."
        )

    member = _get_member_or_denied(request.user)

    # A member can only submit a request for themselves.
    if request.method == "POST":
        form = MarriageRequestForm(request.POST)

        if form.is_valid():
            marriage_request = form.save(commit=False)

            marriage_request.applicant = request.user
            marriage_request.church_member = member
            marriage_request.status = (
                MarriageRequest.STATUS_PENDING
            )

            marriage_request.save()

            messages.success(
                request,
                "Marriage request submitted successfully.",
            )

            return redirect(
                "member_requests:marriage_detail",
                pk=marriage_request.pk,
            )

    else:
        form = MarriageRequestForm()

    return render(
        request,
        "member_requests/marriage/form.html",
        {
            "form": form,
            "title": "New Marriage Request",
        },
    )


@never_cache
@login_required(login_url="accounts:login")
def marriage_request_detail(request, pk):
    """
    Display one marriage request.
    """

    if not can_view_marriage_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to view marriage requests."
        )

    marriage_request = get_object_or_404(
        MarriageRequest.objects.select_related(
            "church_member",
            "applicant",
            "reviewed_by",
        ),
        pk=pk,
    )

    if not _can_view_member_request(
        request.user,
        marriage_request,
    ):
        raise PermissionDenied(
            "You do not have access to this marriage request."
        )

    return render(
        request,
        "member_requests/marriage/detail.html",
        {
            "marriage_request": marriage_request,
        },
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def marriage_request_start_review(request, pk):
    """
    Move a marriage request from Pending to Under Review.
    """

    if not can_review_marriage_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to review marriage requests."
        )

    marriage_request = get_object_or_404(
        MarriageRequest,
        pk=pk,
    )

    if not can_access_request(
        request.user,
        marriage_request,
    ):
        raise PermissionDenied(
            "You do not have access to this marriage request."
        )

    _ensure_status(
        marriage_request,
        [
            MarriageRequest.STATUS_PENDING,
        ],
    )

    marriage_request.status = (
        MarriageRequest.STATUS_UNDER_REVIEW
    )

    marriage_request.reviewed_by = request.user
    marriage_request.reviewed_at = timezone.now()
    marriage_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Marriage request is now under review.",
    )

    return redirect(
        "member_requests:marriage_detail",
        pk=marriage_request.pk,
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def marriage_request_approve(request, pk):
    """
    Approve a marriage request.
    """

    if not can_review_marriage_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to review marriage requests."
        )

    marriage_request = get_object_or_404(
        MarriageRequest,
        pk=pk,
    )

    if not can_access_request(
        request.user,
        marriage_request,
    ):
        raise PermissionDenied(
            "You do not have access to this marriage request."
        )

    _ensure_status(
        marriage_request,
        [
            MarriageRequest.STATUS_UNDER_REVIEW,
        ],
    )

    marriage_request.status = (
        MarriageRequest.STATUS_APPROVED
    )

    marriage_request.reviewed_by = request.user
    marriage_request.reviewed_at = timezone.now()

    marriage_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Marriage request approved successfully.",
    )

    return redirect(
        "member_requests:marriage_detail",
        pk=marriage_request.pk,
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def marriage_request_reject(request, pk):
    """
    Reject a marriage request.
    """

    if not can_review_marriage_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to review marriage requests."
        )

    marriage_request = get_object_or_404(
        MarriageRequest,
        pk=pk,
    )

    if not can_access_request(
        request.user,
        marriage_request,
    ):
        raise PermissionDenied(
            "You do not have access to this marriage request."
        )

    _ensure_status(
        marriage_request,
        [
            MarriageRequest.STATUS_UNDER_REVIEW,
        ],
    )

    review_comment = request.POST.get(
        "review_comment",
        "",
    ).strip()

    if not review_comment:
        messages.error(
            request,
            "A rejection reason is required.",
        )

        return redirect(
            "member_requests:marriage_detail",
            pk=marriage_request.pk,
        )

    marriage_request.status = (
        MarriageRequest.STATUS_REJECTED
    )

    marriage_request.reviewed_by = request.user
    marriage_request.reviewed_at = timezone.now()
    marriage_request.review_comment = review_comment

    marriage_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "review_comment",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Marriage request rejected.",
    )

    return redirect(
        "member_requests:marriage_detail",
        pk=marriage_request.pk,
    )


# ============================================================
# TRANSFER REQUESTS
# ============================================================

@never_cache
@login_required(login_url="accounts:login")
def transfer_request_list(request):
    """
    Display transfer requests accessible to the current user.
    """

    if not can_view_transfer_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to view transfer requests."
        )

    queryset = (
        TransferRequest.objects
        .select_related(
            "church_member",
            "applicant",
            "current_scc",
            "destination_scc",
            "reviewed_by",
        )
        .order_by("-submitted_at")
    )

    member = get_user_church_member(request.user)

    if request.user.is_superuser:
        pass

    elif member:
        queryset = queryset.filter(
            applicant=request.user
        )

    else:
        queryset = queryset.filter(
            church_member__in=get_user_accessible_members(
                request.user
            )
        )

    return render(
        request,
        "member_requests/transfer/list.html",
        {
            "transfer_requests": queryset,
        },
    )


@never_cache
@login_required(login_url="accounts:login")
def transfer_scc_search(request):
    """
    Search active SCCs for the transfer request form.

    Only a small number of matching records are returned,
    preventing thousands of SCCs from being loaded at once.
    """

    if not can_submit_transfer_request(request.user):
        raise PermissionDenied(
            "You do not have permission to submit transfer requests."
        )

    query = request.GET.get("q", "").strip()

    if len(query) < 2:
        return JsonResponse(
            {
                "results": []
            }
        )

    sccs = (
        SmallChristianCommunity.objects
        .filter(
            is_active=True,
            name__icontains=query,
        )
        .select_related(
            "zone__parish__deanery__diocese"
        )
        .order_by("name")[:20]
    )

    results = []

    for scc in sccs:
        results.append(
            {
                "id": str(scc.pk),
                "name": scc.name,
                "zone": scc.zone.name,
                "parish": scc.zone.parish.name,
                "deanery": scc.zone.parish.deanery.name,
                "diocese": scc.zone.parish.deanery.diocese.name,
                "label": (
                    f"{scc.name} — "
                    f"{scc.zone.parish.name} — "
                    f"{scc.zone.name}"
                ),
            }
        )

    return JsonResponse(
        {
            "results": results
        }
    )


@never_cache
@login_required(login_url="accounts:login")
def transfer_request_create(request):
    """
    Submit a new transfer request.
    """

    if not can_submit_transfer_request(request.user):
        raise PermissionDenied(
            "You do not have permission to submit transfer requests."
        )

    member = _get_member_or_denied(request.user)

    current_scc = member.small_christian_community

    if not current_scc:
        messages.error(
            request,
            "Your Church Member record does not have an SCC assigned.",
        )

        return redirect("members:dashboard")

    if request.method == "POST":
        form = TransferRequestForm(
            request.POST,
            current_scc=current_scc,
        )

        if form.is_valid():
            transfer_request = form.save(commit=False)

            transfer_request.applicant = request.user
            transfer_request.church_member = member
            transfer_request.current_scc = current_scc
            transfer_request.status = (
                TransferRequest.STATUS_PENDING
            )

            transfer_request.save()

            messages.success(
                request,
                "Transfer request submitted successfully.",
            )

            return redirect(
                "member_requests:transfer_detail",
                pk=transfer_request.pk,
            )

    else:
        form = TransferRequestForm(
            current_scc=current_scc,
        )

    return render(
        request,
        "member_requests/transfer/form.html",
        {
            "form": form,
            "member": member,
            "current_scc": current_scc,
            "title": "New Transfer Request",
        },
    )


@never_cache
@login_required(login_url="accounts:login")
def transfer_request_detail(request, pk):
    """
    Display one transfer request.
    """

    if not can_view_transfer_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to view transfer requests."
        )

    transfer_request = get_object_or_404(
        TransferRequest.objects.select_related(
            "church_member",
            "applicant",
            "current_scc",
            "destination_scc",
            "reviewed_by",
        ),
        pk=pk,
    )

    if not can_access_transfer_request(
        request.user,
        transfer_request,
    ):
        raise PermissionDenied(
            "You do not have access to this transfer request."
        )

    return render(
        request,
        "member_requests/transfer/detail.html",
        {
            "transfer_request": transfer_request,
        },
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def transfer_request_start_review(request, pk):
    """
    Move a transfer request from Pending to Under Review.
    """

    if not can_review_transfer_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to review transfer requests."
        )

    transfer_request = get_object_or_404(
        TransferRequest,
        pk=pk,
    )

    if not can_access_transfer_request(
        request.user,
        transfer_request,
    ):
        raise PermissionDenied(
            "You do not have access to this transfer request."
        )

    _ensure_status(
        transfer_request,
        [
            TransferRequest.STATUS_PENDING,
        ],
    )

    transfer_request.status = (
        TransferRequest.STATUS_UNDER_REVIEW
    )

    transfer_request.reviewed_by = request.user
    transfer_request.reviewed_at = timezone.now()

    transfer_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Transfer request is now under review.",
    )

    return redirect(
        "member_requests:transfer_detail",
        pk=transfer_request.pk,
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def transfer_request_approve(request, pk):
    """
    Approve a transfer request.

    Approval performs the actual transfer of the
    Church Member to the destination SCC.
    """

    if not can_review_transfer_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to review transfer requests."
        )

    with transaction.atomic():

        transfer_request = (
            TransferRequest.objects
            .select_for_update()
            .select_related(
                "current_scc",
                "destination_scc",
            )
            .filter(pk=pk)
            .first()
        )

        if not transfer_request:
            raise PermissionDenied(
                "Transfer request not found."
            )

        if not can_review_transfer_requests(
            request.user,
            transfer_request,
        ):
            raise PermissionDenied(
                "You do not have access to review this transfer request."
            )

        _ensure_status(
            transfer_request,
            [
                TransferRequest.STATUS_UNDER_REVIEW,
            ],
        )

        # Lock the ChurchMember as well.
        member = (
            ChurchMember.objects
            .select_for_update()
            .get(
                pk=transfer_request.church_member_id
            )
        )

        # The member must still be in the SCC
        # recorded when the request was submitted.
        if (
            member.small_christian_community_id
            != transfer_request.current_scc_id
        ):
            raise PermissionDenied(
                "The member's current SCC has changed. "
                "This transfer request can no longer be approved."
            )

        # Destination must still be active.
        if not transfer_request.destination_scc.is_active:
            raise PermissionDenied(
                "The destination SCC is no longer active."
            )

        # Perform the actual transfer.
        member.small_christian_community = (
            transfer_request.destination_scc
        )

        member.save(
            update_fields=[
                "small_christian_community",
            ]
        )

        # Mark request as approved.
        transfer_request.status = (
            TransferRequest.STATUS_APPROVED
        )

        transfer_request.reviewed_by = request.user
        transfer_request.reviewed_at = timezone.now()

        transfer_request.save(
            update_fields=[
                "status",
                "reviewed_by",
                "reviewed_at",
                "updated_at",
            ]
        )

    messages.success(
        request,
        "Transfer request approved and member transferred successfully.",
    )

    return redirect(
        "member_requests:transfer_detail",
        pk=transfer_request.pk,
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def transfer_request_reject(request, pk):
    """
    Reject a transfer request.
    """

    if not can_review_transfer_requests(request.user):
        raise PermissionDenied(
            "You do not have permission to review transfer requests."
        )

    transfer_request = get_object_or_404(
        TransferRequest,
        pk=pk,
    )

    if not can_access_transfer_request(
        request.user,
        transfer_request,
    ):
        raise PermissionDenied(
            "You do not have access to this transfer request."
        )

    _ensure_status(
        transfer_request,
        [
            TransferRequest.STATUS_UNDER_REVIEW,
        ],
    )

    review_comment = request.POST.get(
        "review_comment",
        "",
    ).strip()

    if not review_comment:
        messages.error(
            request,
            "A rejection reason is required.",
        )

        return redirect(
            "member_requests:transfer_detail",
            pk=transfer_request.pk,
        )

    transfer_request.status = (
        TransferRequest.STATUS_REJECTED
    )

    transfer_request.reviewed_by = request.user
    transfer_request.reviewed_at = timezone.now()
    transfer_request.review_comment = review_comment

    transfer_request.save(
        update_fields=[
            "status",
            "reviewed_by",
            "reviewed_at",
            "review_comment",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Transfer request rejected.",
    )

    return redirect(
        "member_requests:transfer_detail",
        pk=transfer_request.pk,
    )


# ============================================================
# TRAVEL CERTIFICATE REQUESTS
# ============================================================

@never_cache
@login_required(login_url="accounts:login")
def travel_certificate_request_list(request):
    """
    Display travel certificate requests accessible to the user.
    """

    if not can_view_travel_certificate_requests(
        request.user
    ):
        raise PermissionDenied(
            "You do not have permission to view travel certificate requests."
        )

    queryset = (
        TravelCertificateRequest.objects
        .select_related(
            "church_member",
            "applicant",
            "approved_by",
        )
        .order_by("-submitted_at")
    )

    if request.user.is_superuser:
        pass

    elif hasattr(request.user, "church_member"):
        queryset = queryset.filter(
            applicant=request.user
        )

    else:
        queryset = queryset.filter(
            church_member__in=get_user_accessible_members(
                request.user
            )
        )

    return render(
        request,
        "member_requests/travel_certificate/list.html",
        {
            "travel_requests": queryset,
        },
    )


@never_cache
@login_required(login_url="accounts:login")
def travel_certificate_request_create(request):
    """
    Submit a new travel certificate request.
    """

    if not can_submit_travel_certificate_request(
        request.user
    ):
        raise PermissionDenied(
            "You do not have permission to submit travel certificate requests."
        )

    member = _get_member_or_denied(request.user)

    if request.method == "POST":
        form = TravelCertificateRequestForm(
            request.POST
        )

        if form.is_valid():
            travel_request = form.save(commit=False)

            travel_request.applicant = request.user
            travel_request.church_member = member
            travel_request.status = (
                TravelCertificateRequest.STATUS_PENDING
            )

            travel_request.save()

            messages.success(
                request,
                "Travel certificate request submitted successfully.",
            )

            return redirect(
                "member_requests:travel_certificate_detail",
                pk=travel_request.pk,
            )

    else:
        form = TravelCertificateRequestForm()

    return render(
        request,
        "member_requests/travel_certificate/form.html",
        {
            "form": form,
            "title": "New Travel Certificate Request",
        },
    )


@never_cache
@login_required(login_url="accounts:login")
def travel_certificate_request_detail(request, pk):
    """
    Display one travel certificate request.
    """

    if not can_view_travel_certificate_requests(
        request.user
    ):
        raise PermissionDenied(
            "You do not have permission to view travel certificate requests."
        )

    travel_request = get_object_or_404(
        TravelCertificateRequest.objects.select_related(
            "church_member",
            "applicant",
            "approved_by",
        ),
        pk=pk,
    )

    if not can_access_request(
        request.user,
        travel_request,
    ):
        raise PermissionDenied(
            "You do not have access to this travel certificate request."
        )

    return render(
        request,
        "member_requests/travel_certificate/detail.html",
        {
            "travel_request": travel_request,
        },
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def travel_certificate_request_start_review(
    request,
    pk,
):
    """
    Move a travel certificate request from Pending
    to Under Review.
    """

    if not can_approve_travel_certificate_requests(
        request.user
    ):
        raise PermissionDenied(
            "You do not have permission to approve travel certificates."
        )

    travel_request = get_object_or_404(
        TravelCertificateRequest,
        pk=pk,
    )

    if not can_access_request(
        request.user,
        travel_request,
    ):
        raise PermissionDenied(
            "You do not have access to this travel certificate request."
        )

    _ensure_status(
        travel_request,
        [
            TravelCertificateRequest.STATUS_PENDING,
        ],
    )

    travel_request.status = (
        TravelCertificateRequest.STATUS_UNDER_REVIEW
    )

    travel_request.approved_by = request.user
    travel_request.approved_at = timezone.now()

    travel_request.save(
        update_fields=[
            "status",
            "approved_by",
            "approved_at",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Travel certificate request is now under review.",
    )

    return redirect(
        "member_requests:travel_certificate_detail",
        pk=travel_request.pk,
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def travel_certificate_request_approve(
    request,
    pk,
):
    """
    Approve a travel certificate request.
    """

    if not can_approve_travel_certificate_requests(
        request.user
    ):
        raise PermissionDenied(
            "You do not have permission to approve travel certificates."
        )

    with transaction.atomic():

        travel_request = get_object_or_404(
            TravelCertificateRequest.objects.select_for_update(),
            pk=pk,
        )

        if not can_access_request(
            request.user,
            travel_request,
        ):
            raise PermissionDenied(
                "You do not have access to this travel certificate request."
            )

        _ensure_status(
            travel_request,
            [
                TravelCertificateRequest.STATUS_UNDER_REVIEW,
            ],
        )

        travel_request.status = (
            TravelCertificateRequest.STATUS_APPROVED
        )

        travel_request.approved_by = request.user
        travel_request.approved_at = timezone.now()

        # Certificate number generation will be handled
        # by a dedicated service/helper when the certificate
        # document generation module is implemented.
        if not travel_request.certificate_number:
            travel_request.certificate_number = (
                f"TC-{timezone.now():%Y%m%d}-"
                f"{str(travel_request.id)[:8].upper()}"
            )

        travel_request.save(
            update_fields=[
                "status",
                "approved_by",
                "approved_at",
                "certificate_number",
                "updated_at",
            ]
        )

    messages.success(
        request,
        "Travel certificate request approved successfully.",
    )

    return redirect(
        "member_requests:travel_certificate_detail",
        pk=travel_request.pk,
    )


@never_cache
@login_required(login_url="accounts:login")
@require_POST
def travel_certificate_request_reject(
    request,
    pk,
):
    """
    Reject a travel certificate request.
    """

    if not can_approve_travel_certificate_requests(
        request.user
    ):
        raise PermissionDenied(
            "You do not have permission to approve travel certificates."
        )

    travel_request = get_object_or_404(
        TravelCertificateRequest,
        pk=pk,
    )

    if not can_access_request(
        request.user,
        travel_request,
    ):
        raise PermissionDenied(
            "You do not have access to this travel certificate request."
        )

    _ensure_status(
        travel_request,
        [
            TravelCertificateRequest.STATUS_UNDER_REVIEW,
        ],
    )

    review_comment = request.POST.get(
        "review_comment",
        "",
    ).strip()

    if not review_comment:
        messages.error(
            request,
            "A rejection reason is required.",
        )

        return redirect(
            "member_requests:travel_certificate_detail",
            pk=travel_request.pk,
        )

    travel_request.status = (
        TravelCertificateRequest.STATUS_REJECTED
    )

    travel_request.approved_by = request.user
    travel_request.approved_at = timezone.now()
    travel_request.review_comment = review_comment

    travel_request.save(
        update_fields=[
            "status",
            "approved_by",
            "approved_at",
            "review_comment",
            "updated_at",
        ]
    )

    messages.success(
        request,
        "Travel certificate request rejected.",
    )

    return redirect(
        "member_requests:travel_certificate_detail",
        pk=travel_request.pk,
    )


# ============================================================
# ORGANIZATIONAL ACCESS
# ============================================================

def get_user_accessible_members(user):
    """
    Return ChurchMember queryset accessible to an organizational
    administrator/leader.

    This is intentionally kept separate from RBAC permission checks.

    RBAC answers:
        What can the user do?

    This function answers:
        Which members are within the user's organizational scope?
    """

    from members.models import ChurchMember

    if not user or not user.is_authenticated:
        return ChurchMember.objects.none()

    if user.is_superuser:
        return ChurchMember.objects.all()

    profile = getattr(user, "profile", None)

    if not profile:
        return ChurchMember.objects.none()

    queryset = ChurchMember.objects.select_related(
        "small_christian_community__zone__parish__deanery__diocese"
    )

    # Diocese Administrator
    if getattr(profile, "diocese_id", None):
        return queryset.filter(
            small_christian_community__zone__parish__deanery__diocese_id=(
                profile.diocese_id
            )
        )

    # Parish Administrator
    if getattr(profile, "parish_id", None):
        return queryset.filter(
            small_christian_community__zone__parish_id=(
                profile.parish_id
            )
        )

    # SCC / Community Leader
    if getattr(profile, "small_christian_community_id", None):
        return queryset.filter(
            small_christian_community_id=(
                profile.small_christian_community_id
            )
        )

    return ChurchMember.objects.none()