from django.contrib import admin

from .models import (
    ChurchAssociation,
    ChurchMember,
    Deanery,
    Diocese,
    Family,
    LeadershipPosition,
    MemberSacrament,
    Parish,
    Sacrament,
    SmallChristianCommunity,
    Zone,
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


@admin.register(Diocese)
class DioceseAdmin(admin.ModelAdmin):
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


@admin.register(Deanery)
class DeaneryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "diocese",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "diocese",
        "is_active",
    )

    search_fields = (
        "name",
        "diocese__name",
        "description",
    )


@admin.register(Parish)
class ParishAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deanery",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "deanery",
        "is_active",
    )

    search_fields = (
        "name",
        "deanery__name",
        "description",
    )


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parish",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "parish",
        "is_active",
    )

    search_fields = (
        "name",
        "parish__name",
        "description",
    )


@admin.register(SmallChristianCommunity)
class SmallChristianCommunityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "zone",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "zone",
        "is_active",
    )

    search_fields = (
        "name",
        "zone__name",
        "description",
    )


@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "small_christian_community",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "small_christian_community",
        "is_active",
    )

    search_fields = (
        "name",
        "small_christian_community__name",
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
        "family",
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
        "family",
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