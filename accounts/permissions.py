from functools import wraps

from django.core.exceptions import PermissionDenied


def get_user_profile(user):
    """
    Return the CCMIMS UserProfile for an authenticated user.
    """
    if not user.is_authenticated:
        return None

    return getattr(user, "profile", None)


def is_superuser(user):
    """
    Django superusers have unrestricted system access.
    """
    return user.is_authenticated and user.is_superuser


def has_role(user, role):
    """
    Check whether the user has a specific CCMIMS role.
    """
    profile = get_user_profile(user)

    return (
        profile is not None
        and profile.role == role
    )


def is_diocese_admin(user):
    return (
        is_superuser(user)
        or has_role(user, "diocese_admin")
    )


def is_parish_admin(user):
    return (
        is_superuser(user)
        or has_role(user, "parish_admin")
    )


def is_scc_leader(user):
    return (
        is_superuser(user)
        or has_role(user, "scc_leader")
    )


def is_church_member(user):
    return (
        is_superuser(user)
        or has_role(user, "church_member")
    )


def can_manage_members(user):
    """
    Check whether the user has an administrative role
    capable of managing members.
    """
    return (
        is_superuser(user)
        or is_diocese_admin(user)
        or is_parish_admin(user)
        or is_scc_leader(user)
    )


def require_role(*roles):
    """
    Decorator for views that require one or more CCMIMS roles.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                raise PermissionDenied

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            profile = get_user_profile(request.user)

            if profile is None:
                raise PermissionDenied

            if profile.role not in roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

def can_access_diocese(user, diocese):
    """
    Determine whether the user can access a Diocese.
    """

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    profile = get_user_profile(user)

    if profile is None:
        return False

    if profile.role == "diocese_admin":
        return profile.diocese_id == diocese.id

    if profile.role == "parish_admin":
        return (
            profile.parish is not None
            and profile.parish.deanery.diocese_id == diocese.id
        )

    if profile.role == "scc_leader":
        return (
            profile.small_christian_community is not None
            and profile.small_christian_community.zone.parish.deanery.diocese_id
            == diocese.id
        )

    return False

def can_access_parish(user, parish):
    """
    Determine whether the user can access a Parish.
    """

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    profile = get_user_profile(user)

    if profile is None:
        return False

    if profile.role == "diocese_admin":
        return (
            profile.diocese is not None
            and parish.deanery.diocese_id == profile.diocese_id
        )

    if profile.role == "parish_admin":
        return profile.parish_id == parish.id

    if profile.role == "scc_leader":
        return (
            profile.small_christian_community is not None
            and profile.small_christian_community.zone.parish_id
            == parish.id
        )

    return False

def can_access_scc(user, scc):
    """
    Determine whether the user can access a Small Christian Community.
    """

    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    profile = get_user_profile(user)

    if profile is None:
        return False

    if profile.role == "diocese_admin":
        return (
            profile.diocese is not None
            and scc.zone.parish.deanery.diocese_id
            == profile.diocese_id
        )

    if profile.role == "parish_admin":
        return (
            profile.parish is not None
            and scc.zone.parish_id == profile.parish_id
        )

    if profile.role == "scc_leader":
        return profile.small_christian_community_id == scc.id

    return False