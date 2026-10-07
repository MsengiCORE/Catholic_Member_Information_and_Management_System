def user_has_role(user, role_code):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return user.user_roles.filter(
        role__code=role_code,
        role__is_active=True,
        is_active=True,
    ).exists()


def user_has_permission(user, permission_code):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    return user.user_roles.filter(
        is_active=True,
        role__is_active=True,
        role__role_permissions__permission__code=permission_code,
        role__role_permissions__permission__is_active=True,
    ).exists()