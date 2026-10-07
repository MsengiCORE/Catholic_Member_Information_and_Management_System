from django.db.models import Q

from rbac.permissions import user_has_permission
from members.models import ChurchMember


def can_submit_marriage_request(user):
    """
    Check whether a user has permission to submit a marriage request.
    """
    return user_has_permission(
        user,
        "submit_marriage_request",
    )


def can_view_marriage_requests(user):
    """
    Check whether a user has permission to view marriage requests.
    """
    return user_has_permission(
        user,
        "view_marriage_request",
    )


def can_review_marriage_requests(user):
    """
    Check whether a user has permission to review marriage requests.
    """
    return user_has_permission(
        user,
        "review_marriage_request",
    )


def can_submit_transfer_request(user):
    """
    Check whether a user has permission to submit a transfer request.
    """
    return user_has_permission(
        user,
        "submit_transfer_request",
    )


def can_view_transfer_requests(user):
    """
    Check whether a user has permission to view transfer requests.
    """
    return user_has_permission(
        user,
        "view_transfer_request",
    )


def can_review_transfer_requests(user):
    """
    Check whether a user has permission to review transfer requests.
    """
    return user_has_permission(
        user,
        "review_transfer_request",
    )


def can_submit_travel_certificate_request(user):
    """
    Check whether a user has permission to submit
    a travel certificate request.
    """
    return user_has_permission(
        user,
        "submit_travel_certificate_request",
    )


def can_view_travel_certificate_requests(user):
    """
    Check whether a user has permission to view
    travel certificate requests.
    """
    return user_has_permission(
        user,
        "view_travel_certificate_request",
    )


def can_approve_travel_certificate_requests(user):
    """
    Check whether a user has permission to approve
    travel certificate requests.
    """
    return user_has_permission(
        user,
        "approve_travel_certificate_request",
    )


def get_user_church_member(user):
    """
    Return the ChurchMember associated with the authenticated user.

    Returns None when the user is not associated with a ChurchMember.
    """
    if not user or not user.is_authenticated:
        return None

    return (
        ChurchMember.objects
        .select_related(
            "small_christian_community__zone__parish__deanery__diocese"
        )
        .filter(user=user)
        .first()
    )

def is_own_request(user, request_object):
    """
    Check whether the request belongs to the authenticated user.
    """
    if not user or not user.is_authenticated:
        return False

    return request_object.applicant_id == user.id

def user_can_access_member(user, member):
    """
    Check whether the authenticated user can access
    a ChurchMember according to organizational scope.
    """

    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if not user_has_permission(user, "view_member"):
        return False

    profile = getattr(user, "profile", None)

    if not profile:
        return False

    member_scc = member.small_christian_community

    if not member_scc:
        return False

    # Diocese Administrator
    if getattr(profile, "diocese_id", None):
        member_diocese_id = (
            member_scc.zone.parish.deanery.diocese_id
        )

        if member_diocese_id == profile.diocese_id:
            return True

    # Parish Administrator
    if getattr(profile, "parish_id", None):
        member_parish_id = member_scc.zone.parish_id

        if member_parish_id == profile.parish_id:
            return True

    # SCC / Community Leader
    if getattr(profile, "small_christian_community_id", None):
        if (
            member_scc.id
            == profile.small_christian_community_id
        ):
            return True

    return False

def can_access_request(user, request_object):
    """
    Determine whether a user can access a request object.

    Superusers have unrestricted access.

    Church Members can access their own requests.

    Administrators/leaders can access requests belonging
    to members within their organizational scope.
    """

    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if request_object.applicant_id == user.id:
        return True

    return user_can_access_member(
        user,
        request_object.church_member,
    )

def can_access_transfer_request(user, transfer_request):
    """
    Check whether a user can access a transfer request.

    Access is allowed when:
    - the user is the applicant, or
    - the user can access the member, or
    - the user can access the destination/current SCC
      according to their organizational scope.
    """

    if not user or not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if transfer_request.applicant_id == user.id:
        return True

    if user_can_access_member(
        user,
        transfer_request.church_member,
    ):
        return True

    return False

