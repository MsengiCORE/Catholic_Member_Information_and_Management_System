from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from members.models import SmallChristianCommunity

from .models import (
    MarriageRequest,
    TransferRequest,
    TravelCertificateRequest,
)


class MarriageRequestForm(forms.ModelForm):
    """
    Form used by a Church Member to submit a marriage request.
    """

    proposed_spouse_is_catholic = forms.ChoiceField(
        label="Is your proposed spouse Catholic?",
        choices=(
            ("", "Select an option"),
            ("true", "Yes"),
            ("false", "No"),
        ),
        required=True,
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_proposed_spouse_is_catholic",
            }
        ),
    )

    class Meta:
        model = MarriageRequest
        fields = [
            "proposed_spouse_is_catholic",
            "proposed_spouse_digital_offering_number",
            "proposed_spouse_first_name",
            "proposed_spouse_middle_name",
            "proposed_spouse_last_name",
            "proposed_spouse_phone_number",
            "proposed_marriage_date",
            "reason",
        ]

        widgets = {
            "proposed_spouse_digital_offering_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Digital offering number",
                }
            ),
            "proposed_spouse_first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "First name",
                }
            ),
            "proposed_spouse_middle_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Middle name",
                }
            ),
            "proposed_spouse_last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Last name",
                }
            ),
            "proposed_spouse_phone_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Phone number",
                }
            ),
            "proposed_marriage_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Additional information or reason...",
                }
            ),
        }

        labels = {
            "proposed_spouse_is_catholic": "Is the proposed spouse Catholic?",
            "proposed_spouse_digital_offering_number": (
                "Spouse Digital Offering Number"
            ),
            "proposed_spouse_first_name": "Spouse First Name",
            "proposed_spouse_middle_name": "Spouse Middle Name",
            "proposed_spouse_last_name": "Spouse Last Name",
            "proposed_spouse_phone_number": "Spouse Phone Number",
            "proposed_marriage_date": "Proposed Marriage Date",
            "reason": "Additional Information",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["proposed_spouse_is_catholic"].choices = [
            ("", "Select"),
            (True, "Yes"),
            (False, "No"),
        ]

    def clean(self):
        cleaned_data = super().clean()

        is_catholic = cleaned_data.get(
            "proposed_spouse_is_catholic"
        )

        digital_offering_number = cleaned_data.get(
            "proposed_spouse_digital_offering_number"
        )

        first_name = cleaned_data.get(
            "proposed_spouse_first_name"
        )

        middle_name = cleaned_data.get(
            "proposed_spouse_middle_name"
        )

        last_name = cleaned_data.get(
            "proposed_spouse_last_name"
        )

        phone_number = cleaned_data.get(
            "proposed_spouse_phone_number"
        )

        marriage_date = cleaned_data.get(
            "proposed_marriage_date"
        )

        # ---------------------------------------------------------
        # Proposed spouse validation
        # ---------------------------------------------------------

        if is_catholic is None:
            raise ValidationError(
                "Please specify whether the proposed spouse is Catholic."
            )

        if is_catholic is True:
            if not digital_offering_number:
                self.add_error(
                    "proposed_spouse_digital_offering_number",
                    "Digital offering number is required for a Catholic spouse.",
                )

            # Clear non-Catholic fields.
            cleaned_data["proposed_spouse_first_name"] = ""
            cleaned_data["proposed_spouse_middle_name"] = ""
            cleaned_data["proposed_spouse_last_name"] = ""
            cleaned_data["proposed_spouse_phone_number"] = ""

        elif is_catholic is False:
            if not first_name:
                self.add_error(
                    "proposed_spouse_first_name",
                    "First name is required.",
                )

            if not last_name:
                self.add_error(
                    "proposed_spouse_last_name",
                    "Last name is required.",
                )

            if not phone_number:
                self.add_error(
                    "proposed_spouse_phone_number",
                    "Phone number is required.",
                )

            # Clear Catholic-specific field.
            cleaned_data[
                "proposed_spouse_digital_offering_number"
            ] = ""

        # ---------------------------------------------------------
        # Marriage date validation
        # ---------------------------------------------------------

        if marriage_date and marriage_date < timezone.localdate():
            self.add_error(
                "proposed_marriage_date",
                "Proposed marriage date cannot be in the past.",
            )

        return cleaned_data


class TransferRequestForm(forms.ModelForm):
    """
    Form used by a Church Member to submit a transfer request.

    Destination SCCs are loaded through an AJAX search endpoint
    instead of loading all SCC records into the HTML page.
    """

    class Meta:
        model = TransferRequest
        fields = [
            "destination_scc",
            "reason",
        ]

        widgets = {
            "destination_scc": forms.Select(
                attrs={
                    "class": "select select-bordered w-full",
                    "id": "id_destination_scc",
                }
            ),
            "reason": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 5,
                    "placeholder": "Explain why you want to transfer...",
                }
            ),
        }

        labels = {
            "destination_scc": "Destination Small Christian Community",
            "reason": "Reason for Transfer",
        }

    def __init__(self, *args, current_scc=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_scc = current_scc

        # IMPORTANT:
        # Do not load all SCC records here.
        # The destination SCC will be selected through AJAX.
        self.fields["destination_scc"].queryset = (
            SmallChristianCommunity.objects.none()
        )

    def clean_destination_scc(self):
        destination_scc = self.cleaned_data.get("destination_scc")

        if not destination_scc:
            raise ValidationError(
                "Please select a destination SCC."
            )

        if (
            self.current_scc
            and destination_scc.pk == self.current_scc.pk
        ):
            raise ValidationError(
                "Destination SCC must be different from your current SCC."
            )

        if not destination_scc.is_active:
            raise ValidationError(
                "The selected destination SCC is not active."
            )

        return destination_scc

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")

        if not reason or not reason.strip():
            raise ValidationError(
                "Please provide a reason for the transfer."
            )

        return reason.strip()


class TravelCertificateRequestForm(forms.ModelForm):
    """
    Form used by a Church Member to request a travel certificate.
    """

    class Meta:
        model = TravelCertificateRequest
        fields = [
            "destination",
            "purpose",
            "departure_date",
            "return_date",
            "additional_information",
        ]

        widgets = {
            "destination": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Travel destination",
                }
            ),
            "purpose": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Purpose of travel",
                }
            ),
            "departure_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),
            "return_date": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "type": "date",
                }
            ),
            "additional_information": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Additional information...",
                }
            ),
        }

        labels = {
            "destination": "Destination",
            "purpose": "Purpose of Travel",
            "departure_date": "Departure Date",
            "return_date": "Return Date",
            "additional_information": "Additional Information",
        }

    def clean_destination(self):
        destination = self.cleaned_data.get("destination")

        if not destination or not destination.strip():
            raise ValidationError(
                "Destination is required."
            )

        return destination.strip()

    def clean_purpose(self):
        purpose = self.cleaned_data.get("purpose")

        if not purpose or not purpose.strip():
            raise ValidationError(
                "Purpose of travel is required."
            )

        return purpose.strip()

    def clean(self):
        cleaned_data = super().clean()

        departure_date = cleaned_data.get(
            "departure_date"
        )

        return_date = cleaned_data.get(
            "return_date"
        )

        today = timezone.localdate()

        # ---------------------------------------------------------
        # Departure date
        # ---------------------------------------------------------

        if departure_date and departure_date < today:
            self.add_error(
                "departure_date",
                "Departure date cannot be in the past.",
            )

        # ---------------------------------------------------------
        # Return date
        # ---------------------------------------------------------

        if (
            departure_date
            and return_date
            and return_date < departure_date
        ):
            self.add_error(
                "return_date",
                "Return date cannot be before the departure date.",
            )

        return cleaned_data