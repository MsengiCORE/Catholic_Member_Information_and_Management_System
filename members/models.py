import uuid

from django.db import models
from django.contrib.auth.models import User


class ChurchAssociation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class LeadershipPosition(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class Sacrament(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name


class MemberSacrament(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    member = models.ForeignKey(
        "ChurchMember",
        on_delete=models.CASCADE,
        related_name="sacraments"
    )

    sacrament = models.ForeignKey(
        Sacrament,
        on_delete=models.PROTECT,
        related_name="member_records"
    )

    date_received = models.DateField(
        null=True,
        blank=True
    )

    place_received = models.CharField(
        max_length=200,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["member", "sacrament"],
                name="unique_member_sacrament"
            )
        ]

    def __str__(self):
        return f"{self.member} - {self.sacrament}"

class Diocese(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=150,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

class Deanery(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    diocese = models.ForeignKey(
        Diocese,
        on_delete=models.PROTECT,
        related_name="deaneries"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["diocese", "name"],
                name="unique_deanery_per_diocese"
            )
        ]

    def __str__(self):
        return self.name

class Parish(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    deanery = models.ForeignKey(
        Deanery,
        on_delete=models.PROTECT,
        related_name="parishes"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["deanery", "name"],
                name="unique_parish_per_deanery"
            )
        ]

    def __str__(self):
        return self.name

class Zone(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    parish = models.ForeignKey(
        Parish,
        on_delete=models.PROTECT,
        related_name="zones"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parish", "name"],
                name="unique_zone_per_parish"
            )
        ]

    def __str__(self):
        return self.name

class SmallChristianCommunity(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    zone = models.ForeignKey(
        Zone,
        on_delete=models.PROTECT,
        related_name="small_christian_communities"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["zone", "name"],
                name="unique_scc_per_zone"
            )
        ]

    def __str__(self):
        return self.name

class Family(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    small_christian_community = models.ForeignKey(
        SmallChristianCommunity,
        on_delete=models.PROTECT,
        related_name="families"
    )

    name = models.CharField(
        max_length=150
    )

    description = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["small_christian_community", "name"],
                name="unique_family_per_scc"
            )
        ]

    def __str__(self):
        return self.name

class ChurchMember(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="church_member",
    )

    # Identification
    digital_offering_number = models.CharField(
        max_length=50,
        unique=True
    )

    # Personal Information
    first_name = models.CharField(
        max_length=100
    )

    middle_name = models.CharField(
        max_length=100,
        blank=True
    )

    last_name = models.CharField(
        max_length=100
    )

    date_of_birth = models.DateField()

    MARITAL_STATUS_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widow", "Widow"),
        ("widower", "Widower"),
    ]

    marital_status = models.CharField(
        max_length=10,
        choices=MARITAL_STATUS_CHOICES
    )

    # Contact Information
    phone_number = models.CharField(
        max_length=20
    )

    email = models.EmailField(
        blank=True
    )

    # Residence Information
    house_number = models.CharField(
        max_length=50,
        blank=True
    )

    street = models.CharField(
        max_length=150,
        blank=True
    )

    ward = models.CharField(
        max_length=100,
        blank=True
    )

    district = models.CharField(
        max_length=100,
        blank=True
    )

    region = models.CharField(
        max_length=100,
        blank=True
    )

    # Baptism Status
    BAPTISM_STATUS_CHOICES = [
        ("baptized", "Baptized"),
        ("not_baptized", "Not Baptized"),
    ]

    baptism_status = models.CharField(
        max_length=15,
        choices=BAPTISM_STATUS_CHOICES
    )

    # Church Associations
    church_associations = models.ManyToManyField(
        ChurchAssociation,
        blank=True,
        related_name="members"
    )

    # Leadership Positions / Wadhifa
    leadership_positions = models.ManyToManyField(
        LeadershipPosition,
        blank=True,
        related_name="members"
    )

    family = models.CharField(
        max_length=150,
        blank=True,
    )
    # System Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"