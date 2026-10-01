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

from accounts.permissions import get_user_profile

class DioceseForm(forms.ModelForm):

    class Meta:
        model = Diocese
        fields = [
            "name",
            "description",
            "is_active",
        ]

        labels = {
            "name": "Diocese Name",
            "description": "Description",
            "is_active": "Active",
        }

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter Diocese name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full bg-white",
                    "placeholder": "Enter Diocese description (optional)",
                    "rows": 4,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

class DeaneryForm(forms.ModelForm):

    class Meta:
        model = Deanery

        fields = [
            "diocese",
            "name",
            "description",
            "is_active",
        ]

        labels = {
            "diocese": "Diocese",
            "name": "Deanery Name",
            "description": "Description",
            "is_active": "Active",
        }

        widgets = {
            "diocese": forms.Select(
                attrs={
                    "class": "select select-bordered w-full bg-white",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full bg-white",
                    "placeholder": "Enter Deanery name",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full bg-white",
                    "placeholder": "Enter Deanery description (optional)",
                    "rows": 4,
                }
            ),

            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Superuser can see all active Dioceses.
        if user is not None and user.is_superuser:
            self.fields["diocese"].queryset = (
                Diocese.objects
                .filter(is_active=True)
                .order_by("name")
            )

        # Diocese Administrator can only select
        # their assigned Diocese.
        elif user is not None:
            from accounts.permissions import get_user_profile

            profile = get_user_profile(user)

            if (
                profile is not None
                and profile.role == "diocese_admin"
                and profile.diocese_id
            ):
                self.fields["diocese"].queryset = (
                    Diocese.objects
                    .filter(
                        id=profile.diocese_id,
                        is_active=True,
                    )
                    .order_by("name")
                )

            else:
                self.fields["diocese"].queryset = Diocese.objects.none()

        else:
            self.fields["diocese"].queryset = Diocese.objects.none()

class ParishForm(forms.ModelForm):

    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.none(),
        label="Diocese",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_diocese",
            }
        ),
    )

    deanery = forms.ModelChoiceField(
        queryset=Deanery.objects.none(),
        label="Deanery",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_deanery",
            }
        ),
    )

    class Meta:
        model = Parish
        fields = [
            "diocese",
            "deanery",
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter parish name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter parish description",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # Diocese choices
        # -------------------------------------------------
        if user is not None and user.is_superuser:
            self.fields["diocese"].queryset = Diocese.objects.filter(
                is_active=True
            ).order_by("name")

        elif user is not None:
            profile = get_user_profile(user)

            if (
                profile is not None
                and profile.role == "diocese_admin"
                and profile.diocese_id
            ):
                self.fields["diocese"].queryset = Diocese.objects.filter(
                    id=profile.diocese_id,
                    is_active=True,
                )

        # -------------------------------------------------
        # Determine selected Diocese
        # -------------------------------------------------
        selected_diocese_id = None

        if self.is_bound:
            selected_diocese_id = self.data.get("diocese")

        elif self.instance.pk and self.instance.deanery_id:
            selected_diocese_id = self.instance.deanery.diocese_id

        # -------------------------------------------------
        # Deanery choices
        # -------------------------------------------------
        if selected_diocese_id:
            self.fields["deanery"].queryset = Deanery.objects.filter(
                diocese_id=selected_diocese_id,
                is_active=True,
            ).order_by("name")

    def clean(self):
        cleaned_data = super().clean()

        diocese = cleaned_data.get("diocese")
        deanery = cleaned_data.get("deanery")

        if diocese and deanery:

            if deanery.diocese_id != diocese.id:
                self.add_error(
                    "deanery",
                    "The selected Deanery does not belong to the selected Diocese."
                )

        return cleaned_data

class ZoneForm(forms.ModelForm):

    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.none(),
        label="Diocese",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_diocese",
            }
        ),
    )

    deanery = forms.ModelChoiceField(
        queryset=Deanery.objects.none(),
        label="Deanery",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_deanery",
            }
        ),
    )

    parish = forms.ModelChoiceField(
        queryset=Parish.objects.none(),
        label="Parish",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_parish",
            }
        ),
    )

    class Meta:
        model = Zone
        fields = [
            "diocese",
            "deanery",
            "parish",
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter zone name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter zone description",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # Diocese choices
        # -------------------------------------------------

        if user is not None and user.is_superuser:

            self.fields["diocese"].queryset = Diocese.objects.filter(
                is_active=True
            ).order_by("name")

        elif user is not None:

            profile = get_user_profile(user)

            if (
                profile is not None
                and profile.role == "diocese_admin"
                and profile.diocese_id
            ):
                self.fields["diocese"].queryset = Diocese.objects.filter(
                    id=profile.diocese_id,
                    is_active=True,
                )

        # -------------------------------------------------
        # Determine selected Diocese
        # -------------------------------------------------

        selected_diocese_id = None

        if self.is_bound:
            selected_diocese_id = self.data.get("diocese")

        elif self.instance.pk and self.instance.parish_id:
            selected_diocese_id = (
                self.instance.parish.deanery.diocese_id
            )

        # -------------------------------------------------
        # Deanery choices
        # -------------------------------------------------

        if selected_diocese_id:

            self.fields["deanery"].queryset = Deanery.objects.filter(
                diocese_id=selected_diocese_id,
                is_active=True,
            ).order_by("name")

        # -------------------------------------------------
        # Determine selected Deanery
        # -------------------------------------------------

        selected_deanery_id = None

        if self.is_bound:
            selected_deanery_id = self.data.get("deanery")

        elif self.instance.pk and self.instance.parish_id:
            selected_deanery_id = self.instance.parish.deanery_id

        # -------------------------------------------------
        # Parish choices
        # -------------------------------------------------

        if selected_deanery_id:

            self.fields["parish"].queryset = Parish.objects.filter(
                deanery_id=selected_deanery_id,
                is_active=True,
            ).order_by("name")

    def clean(self):
        cleaned_data = super().clean()

        diocese = cleaned_data.get("diocese")
        deanery = cleaned_data.get("deanery")
        parish = cleaned_data.get("parish")

        # -------------------------------------------------
        # Validate Diocese → Deanery
        # -------------------------------------------------

        if diocese and deanery:

            if deanery.diocese_id != diocese.id:
                self.add_error(
                    "deanery",
                    "The selected Deanery does not belong to the selected Diocese."
                )

        # -------------------------------------------------
        # Validate Deanery → Parish
        # -------------------------------------------------

        if deanery and parish:

            if parish.deanery_id != deanery.id:
                self.add_error(
                    "parish",
                    "The selected Parish does not belong to the selected Deanery."
                )

        return cleaned_data

class SmallChristianCommunityForm(forms.ModelForm):

    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.none(),
        label="Diocese",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_diocese",
            }
        ),
    )

    deanery = forms.ModelChoiceField(
        queryset=Deanery.objects.none(),
        label="Deanery",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_deanery",
            }
        ),
    )

    parish = forms.ModelChoiceField(
        queryset=Parish.objects.none(),
        label="Parish",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_parish",
            }
        ),
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.none(),
        label="Zone",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_zone",
            }
        ),
    )

    class Meta:
        model = SmallChristianCommunity
        fields = [
            "diocese",
            "deanery",
            "parish",
            "zone",
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter SCC name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter SCC description",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # Diocese choices
        # -------------------------------------------------

        if user is not None and user.is_superuser:

            self.fields["diocese"].queryset = Diocese.objects.filter(
                is_active=True
            ).order_by("name")

        elif user is not None:

            profile = get_user_profile(user)

            if (
                profile is not None
                and profile.role == "diocese_admin"
                and profile.diocese_id
            ):
                self.fields["diocese"].queryset = Diocese.objects.filter(
                    id=profile.diocese_id,
                    is_active=True,
                )

        # -------------------------------------------------
        # Determine selected Diocese
        # -------------------------------------------------

        selected_diocese_id = None

        if self.is_bound:
            selected_diocese_id = self.data.get("diocese")

        elif self.instance.pk and self.instance.zone_id:
            selected_diocese_id = (
                self.instance.zone.parish.deanery.diocese_id
            )

        # -------------------------------------------------
        # Deanery choices
        # -------------------------------------------------

        if selected_diocese_id:

            self.fields["deanery"].queryset = Deanery.objects.filter(
                diocese_id=selected_diocese_id,
                is_active=True,
            ).order_by("name")

        # -------------------------------------------------
        # Determine selected Deanery
        # -------------------------------------------------

        selected_deanery_id = None

        if self.is_bound:
            selected_deanery_id = self.data.get("deanery")

        elif self.instance.pk and self.instance.zone_id:
            selected_deanery_id = (
                self.instance.zone.parish.deanery_id
            )

        # -------------------------------------------------
        # Parish choices
        # -------------------------------------------------

        if selected_deanery_id:

            self.fields["parish"].queryset = Parish.objects.filter(
                deanery_id=selected_deanery_id,
                is_active=True,
            ).order_by("name")

        # -------------------------------------------------
        # Determine selected Parish
        # -------------------------------------------------

        selected_parish_id = None

        if self.is_bound:
            selected_parish_id = self.data.get("parish")

        elif self.instance.pk and self.instance.zone_id:
            selected_parish_id = self.instance.zone.parish_id

        # -------------------------------------------------
        # Zone choices
        # -------------------------------------------------

        if selected_parish_id:

            self.fields["zone"].queryset = Zone.objects.filter(
                parish_id=selected_parish_id,
                is_active=True,
            ).order_by("name")

    def clean(self):
        cleaned_data = super().clean()

        diocese = cleaned_data.get("diocese")
        deanery = cleaned_data.get("deanery")
        parish = cleaned_data.get("parish")
        zone = cleaned_data.get("zone")

        # -------------------------------------------------
        # Diocese → Deanery
        # -------------------------------------------------

        if diocese and deanery:

            if deanery.diocese_id != diocese.id:
                self.add_error(
                    "deanery",
                    "The selected Deanery does not belong to the selected Diocese."
                )

        # -------------------------------------------------
        # Deanery → Parish
        # -------------------------------------------------

        if deanery and parish:

            if parish.deanery_id != deanery.id:
                self.add_error(
                    "parish",
                    "The selected Parish does not belong to the selected Deanery."
                )

        # -------------------------------------------------
        # Parish → Zone
        # -------------------------------------------------

        if parish and zone:

            if zone.parish_id != parish.id:
                self.add_error(
                    "zone",
                    "The selected Zone does not belong to the selected Parish."
                )

        return cleaned_data

    def save(self, commit=True):
        """
        Save the SCC using the selected Zone.

        The Diocese, Deanery and Parish fields are helper
        fields used for hierarchy selection and validation.
        """

        instance = super().save(commit=False)

        if commit:
            instance.save()

        return instance

class FamilyForm(forms.ModelForm):

    diocese = forms.ModelChoiceField(
        queryset=Diocese.objects.none(),
        label="Diocese",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_diocese",
            }
        ),
    )

    deanery = forms.ModelChoiceField(
        queryset=Deanery.objects.none(),
        label="Deanery",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_deanery",
            }
        ),
    )

    parish = forms.ModelChoiceField(
        queryset=Parish.objects.none(),
        label="Parish",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_parish",
            }
        ),
    )

    zone = forms.ModelChoiceField(
        queryset=Zone.objects.none(),
        label="Zone",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
                "id": "id_zone",
            }
        ),
    )

    small_christian_community = forms.ModelChoiceField(
        queryset=SmallChristianCommunity.objects.none(),
        label="Small Christian Community",
        widget=forms.Select(
            attrs={
                "class": "select select-bordered w-full",
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
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "input input-bordered w-full",
                    "placeholder": "Enter family name",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "textarea textarea-bordered w-full",
                    "rows": 4,
                    "placeholder": "Enter family description",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "checkbox checkbox-primary",
                }
            ),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # -------------------------------------------------
        # Diocese
        # -------------------------------------------------

        if user is not None and user.is_superuser:

            self.fields["diocese"].queryset = Diocese.objects.filter(
                is_active=True
            ).order_by("name")

        elif user is not None:

            profile = get_user_profile(user)

            if (
                profile is not None
                and profile.role == "diocese_admin"
                and profile.diocese_id
            ):
                self.fields["diocese"].queryset = Diocese.objects.filter(
                    id=profile.diocese_id,
                    is_active=True,
                )

        # -------------------------------------------------
        # Selected Diocese
        # -------------------------------------------------

        selected_diocese_id = None

        if self.is_bound:
            selected_diocese_id = self.data.get("diocese")

        elif self.instance.pk and self.instance.small_christian_community_id:
            selected_diocese_id = (
                self.instance
                .small_christian_community
                .zone
                .parish
                .deanery
                .diocese_id
            )

        # -------------------------------------------------
        # Deanery
        # -------------------------------------------------

        if selected_diocese_id:

            self.fields["deanery"].queryset = Deanery.objects.filter(
                diocese_id=selected_diocese_id,
                is_active=True,
            ).order_by("name")

        # -------------------------------------------------
        # Selected Deanery
        # -------------------------------------------------

        selected_deanery_id = None

        if self.is_bound:
            selected_deanery_id = self.data.get("deanery")

        elif self.instance.pk and self.instance.small_christian_community_id:
            selected_deanery_id = (
                self.instance
                .small_christian_community
                .zone
                .parish
                .deanery_id
            )

        # -------------------------------------------------
        # Parish
        # -------------------------------------------------

        if selected_deanery_id:

            self.fields["parish"].queryset = Parish.objects.filter(
                deanery_id=selected_deanery_id,
                is_active=True,
            ).order_by("name")

        # -------------------------------------------------
        # Selected Parish
        # -------------------------------------------------

        selected_parish_id = None

        if self.is_bound:
            selected_parish_id = self.data.get("parish")

        elif self.instance.pk and self.instance.small_christian_community_id:
            selected_parish_id = (
                self.instance
                .small_christian_community
                .zone
                .parish_id
            )

        # -------------------------------------------------
        # Zone
        # -------------------------------------------------

        if selected_parish_id:

            self.fields["zone"].queryset = Zone.objects.filter(
                parish_id=selected_parish_id,
                is_active=True,
            ).order_by("name")

        # -------------------------------------------------
        # Selected Zone
        # -------------------------------------------------

        selected_zone_id = None

        if self.is_bound:
            selected_zone_id = self.data.get("zone")

        elif self.instance.pk and self.instance.small_christian_community_id:
            selected_zone_id = (
                self.instance
                .small_christian_community
                .zone_id
            )

        # -------------------------------------------------
        # SCC
        # -------------------------------------------------

        if selected_zone_id:

            self.fields[
                "small_christian_community"
            ].queryset = SmallChristianCommunity.objects.filter(
                zone_id=selected_zone_id,
                is_active=True,
            ).order_by("name")

    def clean(self):
        cleaned_data = super().clean()

        diocese = cleaned_data.get("diocese")
        deanery = cleaned_data.get("deanery")
        parish = cleaned_data.get("parish")
        zone = cleaned_data.get("zone")
        scc = cleaned_data.get("small_christian_community")

        # -------------------------------------------------
        # Diocese → Deanery
        # -------------------------------------------------

        if diocese and deanery:

            if deanery.diocese_id != diocese.id:
                self.add_error(
                    "deanery",
                    "The selected Deanery does not belong to the selected Diocese."
                )

        # -------------------------------------------------
        # Deanery → Parish
        # -------------------------------------------------

        if deanery and parish:

            if parish.deanery_id != deanery.id:
                self.add_error(
                    "parish",
                    "The selected Parish does not belong to the selected Deanery."
                )

        # -------------------------------------------------
        # Parish → Zone
        # -------------------------------------------------

        if parish and zone:

            if zone.parish_id != parish.id:
                self.add_error(
                    "zone",
                    "The selected Zone does not belong to the selected Parish."
                )

        # -------------------------------------------------
        # Zone → SCC
        # -------------------------------------------------

        if zone and scc:

            if scc.zone_id != zone.id:
                self.add_error(
                    "small_christian_community",
                    "The selected SCC does not belong to the selected Zone."
                )

        return cleaned_data

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
        # Load existing member's organizational hierarchy
        # -----------------------------------------------------

        if self.instance and self.instance.pk:
            scc = self.instance.small_christian_community

            if scc:
                zone = scc.zone
                parish = zone.parish
                deanery = parish.deanery
                diocese = deanery.diocese

                # Diocese
                self.fields["diocese"].initial = diocese

                # Deanery
                self.fields["deanery"].queryset = (
                    Deanery.objects
                    .filter(
                        diocese=diocese,
                        is_active=True,
                    )
                    .order_by("name")
                )
                self.fields["deanery"].initial = deanery

                # Parish
                self.fields["parish"].queryset = (
                    Parish.objects
                    .filter(
                        deanery=deanery,
                        is_active=True,
                    )
                    .order_by("name")
                )
                self.fields["parish"].initial = parish

                # Zone
                self.fields["zone"].queryset = (
                    Zone.objects
                    .filter(
                        parish=parish,
                        is_active=True,
                    )
                    .order_by("name")
                )
                self.fields["zone"].initial = zone

                # SCC
                self.fields["small_christian_community"].queryset = (
                    SmallChristianCommunity.objects
                    .filter(
                        zone=zone,
                        is_active=True,
                    )
                    .order_by("name")
                )
                self.fields["small_christian_community"].initial = scc

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

class ChurchAssociationForm(forms.ModelForm):

    class Meta:
        model = ChurchAssociation

        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Enter association name",
            }),

            "description": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full",
                "placeholder": "Enter association description",
                "rows": 4,
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "checkbox checkbox-primary",
            }),
        }

class MemberAssociationForm(forms.ModelForm):

    class Meta:
        model = ChurchMember
        fields = ["church_associations"]
        widgets = {
            "church_associations": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "space-y-2"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["church_associations"].queryset = (
            ChurchAssociation.objects
            .filter(is_active=True)
            .order_by("name")
        )

class LeadershipPositionForm(forms.ModelForm):

    class Meta:
        model = LeadershipPosition

        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "input input-bordered w-full",
                "placeholder": "Enter leadership position",
            }),

            "description": forms.Textarea(attrs={
                "class": "textarea textarea-bordered w-full",
                "placeholder": "Enter leadership position description",
                "rows": 4,
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "checkbox checkbox-primary",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if not name:
            raise forms.ValidationError(
                "Leadership position name is required."
            )

        return name

    def clean_description(self):
        return self.cleaned_data["description"].strip()

class MemberLeadershipForm(forms.ModelForm):

    class Meta:
        model = ChurchMember
        fields = ["leadership_positions"]

        widgets = {
            "leadership_positions": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "space-y-2"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["leadership_positions"].queryset = (
            LeadershipPosition.objects
            .filter(is_active=True)
            .order_by("name")
        )