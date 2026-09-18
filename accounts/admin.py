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
    )