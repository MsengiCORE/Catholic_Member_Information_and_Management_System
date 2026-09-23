from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "diocese",
        "parish",
        "small_christian_community",
        "created_at",
    )

    list_filter = (
        "role",
        "diocese",
        "parish",
        "small_christian_community",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    # Prevent Django Admin from loading all related records
    # into large HTML <select> elements.
    autocomplete_fields = (
        "diocese",
        "parish",
        "small_christian_community",
    )

    # Avoid extra database queries for displayed relationships.
    list_select_related = (
        "user",
        "diocese",
        "parish",
        "small_christian_community",
    )