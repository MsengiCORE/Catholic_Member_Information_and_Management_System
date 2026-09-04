from datetime import date

from django import forms

from .models import (
    ChurchAssociation,
    ChurchMember,
    LeadershipPosition,
)


class ChurchMemberForm(forms.ModelForm):

    class Meta:
        model = ChurchMember

        fields = [
            "digital_offering_number",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "marital_status",
            "phone_number",
            "email",
            "house_number",
            "street",
            "ward",
            "district",
            "region",
            "baptism_status",
            "church_associations",
            "leadership_positions",
        ]

        labels = {
            "digital_offering_number": "Digital Offering Number",
            "first_name": "First Name",
            "middle_name": "Middle Name",
            "last_name": "Last Name",
            "date_of_birth": "Date of Birth",
            "marital_status": "Marital Status",
            "phone_number": "Phone Number",
            "email": "Email Address",
            "house_number": "House Number",
            "street": "Street",
            "ward": "Ward",
            "district": "District",
            "region": "Region",
            "baptism_status": "Baptism Status",
            "church_associations": "Church Associations",
            "leadership_positions": "Leadership Positions",
        }

        widgets = {
            "digital_offering_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter digital offering number",
                    "required": True,
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter first name",
                    "required": True,
                    "autocomplete": "given-name",
                }
            ),

            "middle_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter middle name",
                    "autocomplete": "additional-name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter last name",
                    "required": True,
                    "autocomplete": "family-name",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "type": "date",
                    "required": True,
                }
            ),

            "marital_status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full bg-white",
                    "required": True,
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "e.g. 0712345678",
                    "required": True,
                    "autocomplete": "tel",
                    "inputmode": "tel",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "example@email.com",
                    "autocomplete": "email",
                    "required": True,
                }
            ),

            "house_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter house number",
                    "required": True,
                }
            ),

            "street": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter street",
                    "required": True,
                }
            ),

            "ward": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter ward",
                    "required": True,
                }
            ),

            "district": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter district",
                    "required": True,
                }
            ),

            "region": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter region",
                    "required": True,
                }
            ),

            "baptism_status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full bg-white",
                    "required": True,
                }
            ),

            "church_associations": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),

            "leadership_positions": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

    def clean_digital_offering_number(self):
        value = self.cleaned_data["digital_offering_number"].strip()

        if not value:
            raise forms.ValidationError(
                "Digital offering number is required."
            )

        return value

    def clean_first_name(self):
        value = self.cleaned_data["first_name"].strip()

        if not value:
            raise forms.ValidationError(
                "First name is required."
            )

        if any(character.isdigit() for character in value):
            raise forms.ValidationError(
                "First name should not contain numbers."
            )

        return value

    def clean_middle_name(self):
        value = self.cleaned_data.get("middle_name", "").strip()

        if value and any(character.isdigit() for character in value):
            raise forms.ValidationError(
                "Middle name should not contain numbers."
            )

        return value

    def clean_last_name(self):
        value = self.cleaned_data["last_name"].strip()

        if not value:
            raise forms.ValidationError(
                "Last name is required."
            )

        if any(character.isdigit() for character in value):
            raise forms.ValidationError(
                "Last name should not contain numbers."
            )

        return value

    def clean_phone_number(self):
        value = self.cleaned_data["phone_number"].strip()

        if not value:
            raise forms.ValidationError(
                "Phone number is required."
            )

        allowed_characters = "0123456789+ -()"

        if any(
            character not in allowed_characters
            for character in value
        ):
            raise forms.ValidationError(
                "Enter a valid phone number."
            )

        return value

    def clean(self):
        cleaned_data = super().clean()

        date_of_birth = cleaned_data.get("date_of_birth")

        if date_of_birth and date_of_birth > date.today():
            self.add_error(
                "date_of_birth",
                "Date of birth cannot be in the future."
            )

        return cleaned_data