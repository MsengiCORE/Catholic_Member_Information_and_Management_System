from django import template

from rbac.permissions import user_has_permission


register = template.Library()


@register.filter
def has_rbac_permission(user, permission_code):
    """
    Return True when the user has the requested active RBAC permission.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return False

    return user_has_permission(user, permission_code)


@register.filter
def has_any_rbac_permission(user, permission_codes):
    """
    Return True when the user has at least one of the comma-separated
    RBAC permissions.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return False

    codes = [
        code.strip()
        for code in str(permission_codes).split(",")
        if code.strip()
    ]

    return any(
        user_has_permission(user, code)
        for code in codes
    )


@register.simple_tag
def rbac_user_roles(user):
    """
    Return the user's active RBAC roles for sidebar/account display.
    """
    if not user or not getattr(user, "is_authenticated", False):
        return []

    if getattr(user, "is_superuser", False):
        return []

    return list(
        user.user_roles
        .filter(
            is_active=True,
            role__is_active=True,
        )
        .select_related("role")
        .order_by("role__name")
        .values(
            "role__id",
            "role__name",
            "role__code",
        )
    )