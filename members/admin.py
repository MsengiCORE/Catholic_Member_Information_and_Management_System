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
        "is_active",
    )

    search_fields = (
        "name",
        "diocese__name",
        "description",
    )

    autocomplete_fields = (
        "diocese",
    )

    list_select_related = (
        "diocese",
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
        "is_active",
    )

    search_fields = (
        "name",
        "deanery__name",
        "description",
    )

    autocomplete_fields = (
        "deanery",
    )

    list_select_related = (
        "deanery",
        "deanery__diocese",
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
        "is_active",
    )

    search_fields = (
        "name",
        "parish__name",
        "description",
    )

    autocomplete_fields = (
        "parish",
    )

    list_select_related = (
        "parish",
        "parish__deanery",
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
        "is_active",
    )

    search_fields = (
        "name",
        "zone__name",
        "description",
    )

    autocomplete_fields = (
        "zone",
    )

    list_select_related = (
        "zone",
        "zone__parish",
    )

    list_per_page = 50


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
        "is_active",
    )

    search_fields = (
        "name",
        "small_christian_community__name",
        "description",
    )

    autocomplete_fields = (
        "small_christian_community",
    )

    list_select_related = (
        "small_christian_community",
        "small_christian_community__zone",
    )

    list_per_page = 50

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
        "small_christian_community",
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
        "small_christian_community__name",
    )

    list_filter = (
        "marital_status",
        "baptism_status",
    )

    autocomplete_fields = (
        "small_christian_community",
    )

    filter_horizontal = (
        "church_associations",
        "leadership_positions",
    )

    list_select_related = (
        "small_christian_community",
        "user",
    )

    list_per_page = 50