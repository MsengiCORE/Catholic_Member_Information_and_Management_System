from datetime import date

from django import forms

from .models import (
    ChurchAssociation,
    ChurchMember,
    Deanery,
    Diocese,
    Family,
    LeadershipPosition,
    Parish,
    SmallChristianCommunity,
    Zone,
)


class FamilyForm(forms.ModelForm):
    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.filter(is_active=True).order_by("name"),
        empty_label="Select Diocese",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_diocese",
            }
        ),
    )

    deanery = forms.ModelChoiceField(
        queryset=Deanery.objects.none(),
        empty_label="Select Deanery",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_deanery",
            }
        ),
    )

    parish = forms.ModelChoiceField(
        queryset=Parish.objects.none(),
        empty_label="Select Parish",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_parish",
            }
        ),
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.none(),
        empty_label="Select Zone",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_zone",
            }
        ),
    )

    small_christian_community = forms.ModelChoiceField(
        queryset=SmallChristianCommunity.objects.none(),
        empty_label="Select Small Christian Community",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_small_christian_community",
            }
        ),
    )

    class Meta:
        model = Family

        fields = [
            "diocese",
            "deanery",
            "parish",
            "zone",
            "small_christian_community",
            "name",
            "description",
        ]

        labels = {
            "diocese": "Diocese",
            "deanery": "Deanery",
            "parish": "Parish",
            "zone": "Zone",
            "small_christian_community": "Small Christian Community",
            "name": "Family Name",
            "description": "Description",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter family name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full bg-white",
                    "placeholder": "Enter family description (optional)",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.is_bound:
            try:
                diocese_id = self.data.get("diocese")

                if diocese_id:
                    self.fields["deanery"].queryset = (
                        Deanery.objects
                        .filter(
                            diocese_id=diocese_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

                deanery_id = self.data.get("deanery")

                if deanery_id:
                    self.fields["parish"].queryset = (
                        Parish.objects
                        .filter(
                            deanery_id=deanery_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

                parish_id = self.data.get("parish")

                if parish_id:
                    self.fields["zone"].queryset = (
                        Zone.objects
                        .filter(
                            parish_id=parish_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

                zone_id = self.data.get("zone")

                if zone_id:
                    self.fields["small_christian_community"].queryset = (
                        SmallChristianCommunity.objects
                        .filter(
                            zone_id=zone_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()

        diocese = cleaned_data.get("diocese")
        deanery = cleaned_data.get("deanery")
        parish = cleaned_data.get("parish")
        zone = cleaned_data.get("zone")
        small_christian_community = cleaned_data.get(
            "small_christian_community"
        )

        if deanery and diocese:
            if deanery.diocese_id != diocese.id:
                self.add_error(
                    "deanery",
                    "The selected Deanery does not belong to the selected Diocese.",
                )

        if parish and deanery:
            if parish.deanery_id != deanery.id:
                self.add_error(
                    "parish",
                    "The selected Parish does not belong to the selected Deanery.",
                )

        if zone and parish:
            if zone.parish_id != parish.id:
                self.add_error(
                    "zone",
                    "The selected Zone does not belong to the selected Parish.",
                )

        if small_christian_community and zone:
            if small_christian_community.zone_id != zone.id:
                self.add_error(
                    "small_christian_community",
                    "The selected Small Christian Community does not belong to the selected Zone.",
                )

        return cleaned_data

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Family name is required."
            )

        return name

    def clean_description(self):
        return self.cleaned_data["description"].strip()

class ChurchMemberForm(forms.ModelForm):
    # ---------------------------------------------------------
    # CHURCH ORGANIZATIONAL HIERARCHY
    # Diocese → Deanery → Parish → Zone → SCC
    # ---------------------------------------------------------

    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.filter(
            is_active=True
        ).order_by("name"),
        required=True,
        label="Diocese",
        empty_label="Select Diocese",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_diocese",
            }
        ),
    )

    deanery = forms.ModelChoiceField(
        queryset=Deanery.objects.none(),
        required=True,
        label="Deanery",
        empty_label="Select Deanery",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_deanery",
            }
        ),
    )

    parish = forms.ModelChoiceField(
        queryset=Parish.objects.none(),
        required=True,
        label="Parish",
        empty_label="Select Parish",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_parish",
            }
        ),
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.none(),
        required=True,
        label="Zone",
        empty_label="Select Zone",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_zone",
            }
        ),
    )

    small_christian_community = forms.ModelChoiceField(
        queryset=SmallChristianCommunity.objects.none(),
        required=True,
        label="Small Christian Community",
        empty_label="Select Small Christian Community",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full bg-white",
                "id": "id_small_christian_community",
            }
        ),
    )

    # Family remains a CharField as requested.
    family = forms.CharField(
        label="Family",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "input input-bordered w-full bg-white",
                "placeholder": "Enter family name",
            }
        ),
    )

    class Meta:
        model = ChurchMember

        fields = [
            "digital_offering_number",
            "first_name",
            "middle_name",
            "last_name",
            "date_of_birth",
            "marital_status",
            "email",
            "house_number",
            "street",
            "ward",
            "district",
            "region",
            "baptism_status",

            # Organizational hierarchy
            "diocese",
            "deanery",
            "parish",
            "zone",
            "small_christian_community",
            "family",

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
            "diocese": "Diocese",
            "deanery": "Deanery",
            "parish": "Parish",
            "zone": "Zone",
            "small_christian_community": "Small Christian Community",
            "family": "Family",
            "church_associations": "Church Associations",
            "leadership_positions": "Leadership Positions",
        }

        widgets = {
            "digital_offering_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter digital offering number",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter first name",
                }
            ),

            "middle_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter middle name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter last name",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "input input-bordered w-full bg-white",
                }
            ),

            "marital_status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full bg-white",
                }
            ),

            "phone_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter phone number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter email address",
                }
            ),

            "house_number": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter house number",
                }
            ),

            "street": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter street",
                }
            ),

            "ward": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter ward",
                }
            ),

            "district": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter district",
                }
            ),

            "region": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter region",
                }
            ),

            "baptism_status": forms.Select(
                attrs={
                    "class": "select select-bordered w-full bg-white",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # -----------------------------------------------------
        # Church Associations
        # -----------------------------------------------------

        self.fields["church_associations"].queryset = (
            ChurchAssociation.objects
            .filter(is_active=True)
            .order_by("name")
        )

        # -----------------------------------------------------
        # Leadership Positions
        # -----------------------------------------------------

        self.fields["leadership_positions"].queryset = (
            LeadershipPosition.objects
            .filter(is_active=True)
            .order_by("name")
        )

        # -----------------------------------------------------
        # Cascading hierarchy for submitted form
        # -----------------------------------------------------

        if self.is_bound:
            try:
                diocese_id = self.data.get("diocese")

                if diocese_id:
                    self.fields["deanery"].queryset = (
                        Deanery.objects
                        .filter(
                            diocese_id=diocese_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

                deanery_id = self.data.get("deanery")

                if deanery_id:
                    self.fields["parish"].queryset = (
                        Parish.objects
                        .filter(
                            deanery_id=deanery_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

                parish_id = self.data.get("parish")

                if parish_id:
                    self.fields["zone"].queryset = (
                        Zone.objects
                        .filter(
                            parish_id=parish_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

                zone_id = self.data.get("zone")

                if zone_id:
                    self.fields[
                        "small_christian_community"
                    ].queryset = (
                        SmallChristianCommunity.objects
                        .filter(
                            zone_id=zone_id,
                            is_active=True,
                        )
                        .order_by("name")
                    )

            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()

        diocese = cleaned_data.get("diocese")
        deanery = cleaned_data.get("deanery")
        parish = cleaned_data.get("parish")
        zone = cleaned_data.get("zone")
        small_christian_community = cleaned_data.get(
            "small_christian_community"
        )

        # Diocese → Deanery
        if deanery and diocese:
            if deanery.diocese_id != diocese.id:
                self.add_error(
                    "deanery",
                    "The selected Deanery does not belong "
                    "to the selected Diocese.",
                )

        # Deanery → Parish
        if parish and deanery:
            if parish.deanery_id != deanery.id:
                self.add_error(
                    "parish",
                    "The selected Parish does not belong "
                    "to the selected Deanery.",
                )

        # Parish → Zone
        if zone and parish:
            if zone.parish_id != parish.id:
                self.add_error(
                    "zone",
                    "The selected Zone does not belong "
                    "to the selected Parish.",
                )

        # Zone → SCC
        if small_christian_community and zone:
            if small_christian_community.zone_id != zone.id:
                self.add_error(
                    "small_christian_community",
                    "The selected Small Christian Community "
                    "does not belong to the selected Zone.",
                )

        return cleaned_data

    def clean_digital_offering_number(self):
        digital_offering_number = (
            self.cleaned_data["digital_offering_number"].strip()
        )

        if not digital_offering_number:
            raise forms.ValidationError(
                "Digital offering number is required."
            )

        return digital_offering_number

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"].strip()

        if not first_name:
            raise forms.ValidationError(
                "First name is required."
            )

        if any(char.isdigit() for char in first_name):
            raise forms.ValidationError(
                "First name cannot contain numbers."
            )

        return first_name

    def clean_middle_name(self):
        middle_name = self.cleaned_data["middle_name"].strip()

        if middle_name and any(char.isdigit() for char in middle_name):
            raise forms.ValidationError(
                "Middle name cannot contain numbers."
            )

        return middle_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"].strip()

        if not last_name:
            raise forms.ValidationError(
                "Last name is required."
            )

        if any(char.isdigit() for char in last_name):
            raise forms.ValidationError(
                "Last name cannot contain numbers."
            )

        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data["phone_number"].strip()

        allowed_characters = "0123456789+ -()"

        if any(
            char not in allowed_characters
            for char in phone_number
        ):
            raise forms.ValidationError(
                "Phone number contains invalid characters."
            )

        return phone_number

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data["date_of_birth"]

        if date_of_birth > date.today():
            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )

        return date_of_birth

    def clean_family(self):
        family = self.cleaned_data.get("family", "").strip()

        if not family:
            return ""

        if any(char.isdigit() for char in family):
            raise forms.ValidationError(
                "Family name cannot contain numbers."
            )

        return family