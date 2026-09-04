from django.contrib import admin

from .models import (
    ChurchAssociation,
    ChurchMember,
    LeadershipPosition,
    MemberSacrament,
    Sacrament,
)


@admin.register(ChurchAssociation)
class ChurchAssociationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(LeadershipPosition)
class LeadershipPositionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(Sacrament)
class SacramentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "description",
    )


@admin.register(MemberSacrament)
class MemberSacramentAdmin(admin.ModelAdmin):
    list_display = (
        "member",
        "sacrament",
        "date_received",
        "place_received",
        "created_at",
    )

    list_filter = (
        "sacrament",
        "date_received",
    )

    search_fields = (
        "member__digital_offering_number",
        "member__first_name",
        "member__middle_name",
        "member__last_name",
        "place_received",
    )


@admin.register(ChurchMember)
class ChurchMemberAdmin(admin.ModelAdmin):

    list_display = (
        "digital_offering_number",
        "first_name",
        "middle_name",
        "last_name",
        "phone_number",
        "marital_status",
        "baptism_status",
        "created_at",
    )

    search_fields = (
        "digital_offering_number",
        "first_name",
        "middle_name",
        "last_name",
        "phone_number",
        "email",
    )

    list_filter = (
        "marital_status",
        "baptism_status",
        "church_associations",
        "leadership_positions",
    )

    filter_horizontal = (
        "church_associations",
        "leadership_positions",
    )