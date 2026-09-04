import uuid

from django.db import models


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


class ChurchMember(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
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

    # System Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"