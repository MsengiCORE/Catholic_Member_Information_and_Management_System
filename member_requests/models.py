import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class MarriageRequest(models.Model):
    """
    Request submitted by a church member for marriage-related processing.
    """

    STATUS_PENDING = "pending"
    STATUS_UNDER_REVIEW = "under_review"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_UNDER_REVIEW, "Under Review"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # User who submitted the request
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="submitted_marriage_requests",
    )

    # Church member associated with the request
    church_member = models.ForeignKey(
        "members.ChurchMember",
        on_delete=models.PROTECT,
        related_name="marriage_requests",
    )

    # Proposed spouse details
    proposed_spouse_is_catholic = models.BooleanField(
        default=False,
    )

    proposed_spouse_digital_offering_number = models.CharField(
        max_length=100,
        blank=True,
    )

    proposed_spouse_first_name = models.CharField(
        max_length=100,
        blank=True,
    )

    proposed_spouse_middle_name = models.CharField(
        max_length=100,
        blank=True,
    )

    proposed_spouse_last_name = models.CharField(
        max_length=100,
        blank=True,
    )

    proposed_spouse_phone_number = models.CharField(
        max_length=30,
        blank=True,
    )

    proposed_marriage_date = models.DateField(
        null=True,
        blank=True,
    )

    reason = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    # Review information
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_marriage_requests",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    review_comment = models.TextField(
        blank=True,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Marriage Request"
        verbose_name_plural = "Marriage Requests"

    def __str__(self):
        return (
            f"Marriage Request - "
            f"{self.church_member.first_name} "
            f"{self.church_member.last_name}"
        )


class TransferRequest(models.Model):
    """
    Request submitted by a church member to move
    from the current SCC to another SCC.
    """

    STATUS_PENDING = "pending"
    STATUS_UNDER_REVIEW = "under_review"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_UNDER_REVIEW, "Under Review"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # User who submitted the request
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="submitted_transfer_requests",
    )

    # Member being transferred
    church_member = models.ForeignKey(
        "members.ChurchMember",
        on_delete=models.PROTECT,
        related_name="transfer_requests",
    )

    # Current organization
    current_scc = models.ForeignKey(
        "members.SmallChristianCommunity",
        on_delete=models.PROTECT,
        related_name="outgoing_transfer_requests",
    )

    # Requested destination
    destination_scc = models.ForeignKey(
        "members.SmallChristianCommunity",
        on_delete=models.PROTECT,
        related_name="incoming_transfer_requests",
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    # Review information
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_transfer_requests",
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    review_comment = models.TextField(
        blank=True,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Transfer Request"
        verbose_name_plural = "Transfer Requests"

    def clean(self):
        if (
            self.current_scc_id
            and self.destination_scc_id
            and self.current_scc_id == self.destination_scc_id
        ):
            raise ValidationError(
                {
                    "destination_scc": (
                        "Destination SCC must be different "
                        "from the current SCC."
                    )
                }
            )

    def __str__(self):
        return (
            f"Transfer Request - "
            f"{self.church_member.first_name} "
            f"{self.church_member.last_name}"
        )


class TravelCertificateRequest(models.Model):
    """
    Request submitted by a church member for a travel certificate.
    """

    STATUS_PENDING = "pending"
    STATUS_UNDER_REVIEW = "under_review"
    STATUS_APPROVED = "approved"
    STATUS_REJECTED = "rejected"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_UNDER_REVIEW, "Under Review"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_REJECTED, "Rejected"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    # User who submitted the request
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="submitted_travel_certificate_requests",
    )

    # Church member requesting the certificate
    church_member = models.ForeignKey(
        "members.ChurchMember",
        on_delete=models.PROTECT,
        related_name="travel_certificate_requests",
    )

    destination = models.CharField(
        max_length=255,
    )

    purpose = models.TextField()

    departure_date = models.DateField()

    return_date = models.DateField(
        null=True,
        blank=True,
    )

    additional_information = models.TextField(
        blank=True,
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    # Generated when the request is approved
    certificate_number = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
    )

    # Approval information
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_travel_certificate_requests",
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    review_comment = models.TextField(
        blank=True,
    )

    submitted_at = models.DateTimeField(
        auto_now_add=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Travel Certificate Request"
        verbose_name_plural = "Travel Certificate Requests"

    def __str__(self):
        return (
            f"Travel Certificate Request - "
            f"{self.church_member.first_name} "
            f"{self.church_member.last_name}"
        )