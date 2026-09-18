from django.conf import settings
from django.db import models

from members.models import Diocese, Parish, SmallChristianCommunity


class UserProfile(models.Model):

    class Role(models.TextChoices):
        DIOCESE_ADMIN = "diocese_admin", "Diocese Administrator"
        PARISH_ADMIN = "parish_admin", "Parish Administrator"
        SCC_LEADER = "scc_leader", "SCC / Community Leader"
        CHURCH_MEMBER = "church_member", "Church Member"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.CHURCH_MEMBER
    )

    # Organizational scope
    diocese = models.ForeignKey(
        Diocese,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profiles"
    )

    parish = models.ForeignKey(
        Parish,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profiles"
    )

    small_christian_community = models.ForeignKey(
        SmallChristianCommunity,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profiles"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"