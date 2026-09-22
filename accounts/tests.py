from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from members.models import (
    Diocese,
    Deanery,
    Parish,
    Zone,
    SmallChristianCommunity,
    ChurchMember,
)

from accounts.models import UserProfile
from accounts.permissions import (
    can_access_member,
    get_accessible_members,
)

class MemberAccessPermissionTests(TestCase):

    def setUp(self):

        User = get_user_model()

        # -----------------------------------------------------
        # Diocese
        # -----------------------------------------------------
        self.diocese_1 = Diocese.objects.create(
            name="Test Diocese One"
        )

        self.diocese_2 = Diocese.objects.create(
            name="Test Diocese Two"
        )

        # -----------------------------------------------------
        # Deaneries
        # -----------------------------------------------------
        self.deanery_1 = Deanery.objects.create(
            diocese=self.diocese_1,
            name="Test Deanery One"
        )

        self.deanery_2 = Deanery.objects.create(
            diocese=self.diocese_2,
            name="Test Deanery Two"
        )

        # -----------------------------------------------------
        # Parishes
        # -----------------------------------------------------
        self.parish_1 = Parish.objects.create(
            deanery=self.deanery_1,
            name="Test Parish One"
        )

        self.parish_2 = Parish.objects.create(
            deanery=self.deanery_2,
            name="Test Parish Two"
        )

        # -----------------------------------------------------
        # Zones
        # -----------------------------------------------------
        self.zone_1 = Zone.objects.create(
            parish=self.parish_1,
            name="Test Zone One"
        )

        self.zone_2 = Zone.objects.create(
            parish=self.parish_2,
            name="Test Zone Two"
        )

        # -----------------------------------------------------
        # SCCs
        # -----------------------------------------------------
        self.scc_1 = SmallChristianCommunity.objects.create(
            zone=self.zone_1,
            name="Test SCC One"
        )

        self.scc_2 = SmallChristianCommunity.objects.create(
            zone=self.zone_2,
            name="Test SCC Two"
        )

        # -----------------------------------------------------
        # Users
        # -----------------------------------------------------
        self.superuser = User.objects.create_superuser(
            username="test_superuser",
            password="testpass123"
        )

        self.diocese_admin = User.objects.create_user(
            username="diocese_admin",
            password="testpass123"
        )

        self.parish_admin = User.objects.create_user(
            username="parish_admin",
            password="testpass123"
        )

        self.scc_leader = User.objects.create_user(
            username="scc_leader",
            password="testpass123"
        )

        self.church_member_user = User.objects.create_user(
            username="church_member",
            password="testpass123"
        )

        self.other_member_user = User.objects.create_user(
            username="other_member",
            password="testpass123"
        )

        # -----------------------------------------------------
        # User profiles
        # -----------------------------------------------------
        diocese_profile = UserProfile.objects.get(user=self.diocese_admin)
        diocese_profile.role = UserProfile.Role.DIOCESE_ADMIN
        diocese_profile.diocese = self.diocese_1
        diocese_profile.save()

        parish_profile = UserProfile.objects.get(user=self.parish_admin)
        parish_profile.role = UserProfile.Role.PARISH_ADMIN
        parish_profile.parish = self.parish_1
        parish_profile.diocese = self.diocese_1
        parish_profile.save()

        scc_profile = UserProfile.objects.get(user=self.scc_leader)
        scc_profile.role = UserProfile.Role.SCC_LEADER
        scc_profile.small_christian_community = self.scc_1
        scc_profile.parish = self.parish_1
        scc_profile.diocese = self.diocese_1
        scc_profile.save()

        church_member_profile = UserProfile.objects.get(
            user=self.church_member_user
        )
        church_member_profile.role = UserProfile.Role.CHURCH_MEMBER
        church_member_profile.save()

        other_member_profile = UserProfile.objects.get(
            user=self.other_member_user
        )
        other_member_profile.role = UserProfile.Role.CHURCH_MEMBER
        other_member_profile.save()

        # -----------------------------------------------------
        # Members
        # -----------------------------------------------------
        self.member_1 = ChurchMember.objects.create(
            user=self.church_member_user,
            digital_offering_number="TEST-001",
            first_name="Member",
            middle_name="One",
            last_name="Test",
            date_of_birth="1995-01-01",
            marital_status="single",
            phone_number="0711000001",
            ward="Ward One",
            district="District One",
            region="Region One",
            baptism_status="baptized",
            small_christian_community=self.scc_1,
            family="Family One",
        )

        self.member_2 = ChurchMember.objects.create(
            user=self.other_member_user,
            digital_offering_number="TEST-002",
            first_name="Member",
            middle_name="Two",
            last_name="Test",
            date_of_birth="1996-01-01",
            marital_status="single",
            phone_number="0711000002",
            ward="Ward Two",
            district="District Two",
            region="Region Two",
            baptism_status="baptized",
            small_christian_community=self.scc_2,
            family="Family Two",
        )

    def test_superuser_can_access_any_member(self):

        self.assertTrue(
            can_access_member(
                self.superuser,
                self.member_1
            )
        )

        self.assertTrue(
            can_access_member(
                self.superuser,
                self.member_2
            )
        )


    def test_diocese_admin_can_access_members_in_own_diocese(self):

        self.assertTrue(
            can_access_member(
                self.diocese_admin,
                self.member_1
            )
        )

        self.assertFalse(
            can_access_member(
                self.diocese_admin,
                self.member_2
            )
        )


    def test_parish_admin_can_access_members_in_own_parish(self):

        self.assertTrue(
            can_access_member(
                self.parish_admin,
                self.member_1
            )
        )

        self.assertFalse(
            can_access_member(
                self.parish_admin,
                self.member_2
            )
        )


    def test_scc_leader_can_access_members_in_own_scc(self):

        self.assertTrue(
            can_access_member(
                self.scc_leader,
                self.member_1
            )
        )

        self.assertFalse(
            can_access_member(
                self.scc_leader,
                self.member_2
            )
        )


    def test_church_member_can_access_only_own_profile(self):

        self.assertTrue(
            can_access_member(
                self.church_member_user,
                self.member_1
            )
        )

        self.assertFalse(
            can_access_member(
                self.church_member_user,
                self.member_2
            )
        )


    def test_accessible_members_queryset_is_scoped(self):

        queryset = ChurchMember.objects.all()

        diocese_members = get_accessible_members(
            self.diocese_admin,
            queryset
        )

        self.assertIn(
            self.member_1,
            diocese_members
        )

        self.assertNotIn(
            self.member_2,
            diocese_members
        )

class MemberScopeViewTests(TestCase):

    def setUp(self):
        User = get_user_model()

        # -----------------------------------------------------
        # Diocese
        # -----------------------------------------------------
        self.diocese_1 = Diocese.objects.create(
            name="View Test Diocese One"
        )

        self.diocese_2 = Diocese.objects.create(
            name="View Test Diocese Two"
        )

        # -----------------------------------------------------
        # Deaneries
        # -----------------------------------------------------
        self.deanery_1 = Deanery.objects.create(
            diocese=self.diocese_1,
            name="View Test Deanery One"
        )

        self.deanery_2 = Deanery.objects.create(
            diocese=self.diocese_2,
            name="View Test Deanery Two"
        )

        # -----------------------------------------------------
        # Parishes
        # -----------------------------------------------------
        self.parish_1 = Parish.objects.create(
            deanery=self.deanery_1,
            name="View Test Parish One"
        )

        self.parish_2 = Parish.objects.create(
            deanery=self.deanery_2,
            name="View Test Parish Two"
        )

        # -----------------------------------------------------
        # Zones
        # -----------------------------------------------------
        self.zone_1 = Zone.objects.create(
            parish=self.parish_1,
            name="View Test Zone One"
        )

        self.zone_2 = Zone.objects.create(
            parish=self.parish_2,
            name="View Test Zone Two"
        )

        # -----------------------------------------------------
        # SCCs
        # -----------------------------------------------------
        self.scc_1 = SmallChristianCommunity.objects.create(
            zone=self.zone_1,
            name="View Test SCC One"
        )

        self.scc_2 = SmallChristianCommunity.objects.create(
            zone=self.zone_2,
            name="View Test SCC Two"
        )

        # -----------------------------------------------------
        # Users
        # -----------------------------------------------------
        self.superuser = User.objects.create_superuser(
            username="view_superuser",
            password="testpass123"
        )

        self.diocese_admin = User.objects.create_user(
            username="view_diocese_admin",
            password="testpass123"
        )

        self.parish_admin = User.objects.create_user(
            username="view_parish_admin",
            password="testpass123"
        )

        self.scc_leader = User.objects.create_user(
            username="view_scc_leader",
            password="testpass123"
        )

        self.church_member_user = User.objects.create_user(
            username="view_church_member",
            password="testpass123"
        )

        self.other_member_user = User.objects.create_user(
            username="view_other_member",
            password="testpass123"
        )

        # -----------------------------------------------------
        # Profiles
        # -----------------------------------------------------
        profile = UserProfile.objects.get(user=self.diocese_admin)
        profile.role = UserProfile.Role.DIOCESE_ADMIN
        profile.diocese = self.diocese_1
        profile.save()

        profile = UserProfile.objects.get(user=self.parish_admin)
        profile.role = UserProfile.Role.PARISH_ADMIN
        profile.diocese = self.diocese_1
        profile.parish = self.parish_1
        profile.save()

        profile = UserProfile.objects.get(user=self.scc_leader)
        profile.role = UserProfile.Role.SCC_LEADER
        profile.diocese = self.diocese_1
        profile.parish = self.parish_1
        profile.small_christian_community = self.scc_1
        profile.save()

        profile = UserProfile.objects.get(user=self.church_member_user)
        profile.role = UserProfile.Role.CHURCH_MEMBER
        profile.save()

        profile = UserProfile.objects.get(user=self.other_member_user)
        profile.role = UserProfile.Role.CHURCH_MEMBER
        profile.save()

        # -----------------------------------------------------
        # Members
        # -----------------------------------------------------
        self.member_1 = ChurchMember.objects.create(
            user=self.church_member_user,
            digital_offering_number="VIEW-001",
            first_name="View",
            middle_name="Member",
            last_name="One",
            date_of_birth="1995-01-01",
            marital_status="single",
            phone_number="0711000011",
            ward="Ward One",
            district="District One",
            region="Region One",
            baptism_status="baptized",
            small_christian_community=self.scc_1,
            family="Family One",
        )

        self.member_2 = ChurchMember.objects.create(
            user=self.other_member_user,
            digital_offering_number="VIEW-002",
            first_name="View",
            middle_name="Member",
            last_name="Two",
            date_of_birth="1996-01-01",
            marital_status="single",
            phone_number="0711000012",
            ward="Ward Two",
            district="District Two",
            region="Region Two",
            baptism_status="baptized",
            small_christian_community=self.scc_2,
            family="Family Two",
        )

    # ---------------------------------------------------------
    # MEMBER DETAIL
    # ---------------------------------------------------------

    def test_diocese_admin_can_view_member_in_own_diocese(self):
        self.client.force_login(self.diocese_admin)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_1.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_diocese_admin_cannot_view_member_outside_own_diocese(self):
        self.client.force_login(self.diocese_admin)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_2.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_parish_admin_can_view_member_in_own_parish(self):
        self.client.force_login(self.parish_admin)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_1.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_parish_admin_cannot_view_member_outside_own_parish(self):
        self.client.force_login(self.parish_admin)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_2.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_scc_leader_can_view_member_in_own_scc(self):
        self.client.force_login(self.scc_leader)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_1.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_scc_leader_cannot_view_member_outside_own_scc(self):
        self.client.force_login(self.scc_leader)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_2.pk})
        )

        self.assertEqual(response.status_code, 403)

    def test_church_member_can_view_own_profile(self):
        self.client.force_login(self.church_member_user)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_1.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_church_member_cannot_view_another_member(self):
        self.client.force_login(self.church_member_user)

        response = self.client.get(
            reverse("members:member_detail", kwargs={"pk": self.member_2.pk})
        )

        self.assertEqual(response.status_code, 403)

    # ---------------------------------------------------------
    # MEMBER LIST
    # ---------------------------------------------------------

    def test_diocese_admin_member_list_is_scoped(self):
        self.client.force_login(self.diocese_admin)

        response = self.client.get(
            reverse("members:member_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VIEW-001")
        self.assertNotContains(response, "VIEW-002")

    def test_parish_admin_member_list_is_scoped(self):
        self.client.force_login(self.parish_admin)

        response = self.client.get(
            reverse("members:member_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VIEW-001")
        self.assertNotContains(response, "VIEW-002")

    def test_scc_leader_member_list_is_scoped(self):
        self.client.force_login(self.scc_leader)

        response = self.client.get(
            reverse("members:member_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VIEW-001")
        self.assertNotContains(response, "VIEW-002")

    def test_church_member_member_list_is_scoped(self):
        self.client.force_login(self.church_member_user)

        response = self.client.get(
            reverse("members:member_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "VIEW-001")
        self.assertNotContains(response, "VIEW-002")