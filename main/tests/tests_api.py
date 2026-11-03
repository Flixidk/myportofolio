import uuid
from datetime import date

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Experience, Skill


class ExperienceAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.experience = Experience.objects.create(
            title="Backend Intern", description="Built REST APIs",
            category="internship", started_at=date(2025, 6, 1), ended_at=date(2025, 9, 1),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", args=[self.experience.id])
        self.star_url = reverse("api:experience-star", args=[self.experience.id])
        self.payload = {
            "title": "Freelance Developer", "description": "Built portfolio sites",
            "category": "freelance", "started_at": "2024-01-01", "ended_at": "2024-12-31",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.experience.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "BACK"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_experience(self):
        url = reverse("api:experience-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Backend Intern")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Experience.objects.filter(pk=response.data["id"]).exists())
        self.assertEqual(response.data["category"], "freelance")

    def test_started_at_is_optional(self):
        self.client.force_authenticate(user=self.owner)
        payload = {k: v for k, v in self.payload.items() if k != "started_at"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(response.data["started_at"])

    def test_category_defaults_to_full_time(self):
        self.client.force_authenticate(user=self.owner)
        payload = {k: v for k, v in self.payload.items() if k != "category"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["category"], "full-time")

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"description": ""}, "description"),
            ({"category": "astronaut"}, "category"),
            ({"started_at": "not-a-date"}, "started_at"),
            ({"ended_at": "31/12/2024"}, "ended_at"),
            ({"ended_at": None}, "ended_at"),   # ended_at must be filled
            ({"ended_at": ""}, "ended_at"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_ended_at_is_required(self):
        self.client.force_authenticate(user=self.owner)
        payload = {k: v for k, v in self.payload.items() if k != "ended_at"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ended_at", response.data)

    def test_html_is_stripped(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload,
            "title": "<b>Dev</b>",
            "description": "<script>alert(1)</script>Hello",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "Dev")
        self.assertNotIn("<", response.data["description"])
        self.assertTrue(response.data["description"].endswith("Hello"))

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")
        self.assertEqual(self.experience.description, "Built REST APIs")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Experience.objects.filter(pk=self.experience.id).exists())

    def test_patch_cannot_clear_ended_at(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"ended_at": None}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.ended_at, date(2025, 9, 1))

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(response.data["starred_by_names"], "visitor")
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        forged_id = str(uuid.uuid4())
        response = self.client.post(self.list_url, {
            **self.payload, "id": forged_id, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotEqual(response.data["id"], forged_id)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["starred_by_names"], "")

    def test_editor_can_patch_but_cannot_create_or_delete_experiences(self):
        editor_group, _ = Group.objects.get_or_create(name="Editors")
        self.visitor.groups.add(editor_group)
        self.client.force_authenticate(user=self.visitor)
        patched = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(patched.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Changed")

        created = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(created.status_code, status.HTTP_403_FORBIDDEN)
        deleted = self.client.delete(self.detail_url)
        self.assertEqual(deleted.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SkillAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="skill-owner", password="test-password", email="skill-owner@example.com",
        )
        self.visitor = User.objects.create_user(username="skill-visitor", password="test-password")
        self.skill = Skill.objects.create(
            title="Python", category="backend", description="Basic syntax",
            icon_path="https://example.com/python.svg", order=1,
        )
        self.list_url = reverse("api:skill-list")
        self.detail_url = reverse("api:skill-detail", args=[self.skill.id])
        self.endorse_url = reverse("api:skill-endorse", args=[self.skill.id])
        self.payload = {
            "title": "Django", "description": "Web framework", "category": "backend",
            "icon_path": "https://example.com/django.svg", "order": 2,
        }

    def test_public_list_category_filter_detail_head_and_missing_skill(self):
        Skill.objects.create(title="HTML", category="frontend", order=2)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["title"] for item in response.data], ["Python", "HTML"])
        self.assertEqual(self.client.get(self.list_url, {"cat": "backend"}).data[0]["title"], "Python")
        self.assertEqual(self.client.get(self.list_url, {"cat": "unknown"}).data, [])
        self.assertEqual(self.client.head(self.list_url).status_code, status.HTTP_200_OK)

        detail = self.client.get(self.detail_url)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["category"], "backend")
        self.assertEqual(self.client.head(self.detail_url).status_code, status.HTTP_200_OK)
        missing = reverse("api:skill-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(missing).status_code, status.HTTP_404_NOT_FOUND)

    def test_visitor_and_regular_user_cannot_write_and_database_is_unchanged(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            created = self.client.post(self.list_url, self.payload, format="json")
            self.assertEqual(created.status_code, status.HTTP_403_FORBIDDEN)
            changed = self.client.patch(self.detail_url, {"title": "Tampered"}, format="json")
            self.assertEqual(changed.status_code, status.HTTP_403_FORBIDDEN)
            deleted = self.client.delete(self.detail_url)
            self.assertEqual(deleted.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(Skill.objects.count(), 1)
            self.assertTrue(Skill.objects.filter(pk=self.skill.pk, title="Python").exists())

    def test_editor_can_patch_but_cannot_create_or_delete(self):
        group, _ = Group.objects.get_or_create(name="Editors")
        self.visitor.groups.add(group)
        self.client.force_authenticate(user=self.visitor)

        patched = self.client.patch(self.detail_url, {"title": "Python 3"}, format="json")
        self.assertEqual(patched.status_code, status.HTTP_200_OK)
        self.skill.refresh_from_db()
        self.assertEqual(self.skill.title, "Python 3")

        created = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(created.status_code, status.HTTP_403_FORBIDDEN)
        deleted = self.client.delete(self.detail_url)
        self.assertEqual(deleted.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Skill.objects.count(), 1)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk, title="Python 3").exists())

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        created = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(created.status_code, status.HTTP_201_CREATED)
        created_skill_id = created.data["id"]
        self.assertTrue(Skill.objects.filter(pk=created_skill_id, title="Django").exists())

        update_url = reverse("api:skill-detail", args=[created_skill_id])
        replaced = self.client.put(update_url, self.payload, format="json")
        self.assertEqual(replaced.status_code, status.HTTP_200_OK)
        self.assertTrue(Skill.objects.filter(pk=created_skill_id, title="Django").exists())
        deleted = self.client.delete(update_url)
        self.assertEqual(deleted.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Skill.objects.filter(pk=created_skill_id).exists())

    def test_validation_and_html_sanitization(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in (
            ({"title": "   "}, "title"),
            ({"title": "<b></b>"}, "title"),
            ({"category": "astronaut"}, "category"),
        ):
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, changes)
            self.assertIn(field, response.data)
            self.assertEqual(Skill.objects.count(), 1)

        sanitized = self.client.post(self.list_url, {
            **self.payload,
            "title": "<b>API</b>",
            "description": "<script>alert(1)</script>Safe",
            "icon_path": "<b>https://example.com/api.svg</b>",
        }, format="json")
        self.assertEqual(sanitized.status_code, status.HTTP_201_CREATED)
        self.assertEqual(sanitized.data["title"], "API")
        self.assertEqual(sanitized.data["description"], "alert(1)Safe")
        self.assertEqual(sanitized.data["icon_path"], "https://example.com/api.svg")
        self.assertEqual(Skill.objects.count(), 2)

    def test_endorsement_requires_login_and_toggles(self):
        denied = self.client.post(self.endorse_url)
        self.assertEqual(denied.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(self.skill.endorsed_by.exists())

        self.client.force_authenticate(user=self.visitor)
        endorsed = self.client.post(self.endorse_url)
        self.assertEqual(endorsed.status_code, status.HTTP_200_OK)
        self.assertTrue(endorsed.data["is_endorsed"])
        self.assertEqual(endorsed.data["endorse_count"], 1)
        self.assertEqual(endorsed.data["endorsed_by_names"], "skill-visitor")
        self.assertTrue(self.skill.endorsed_by.filter(pk=self.visitor.pk).exists())

        removed = self.client.post(self.endorse_url)
        self.assertEqual(removed.status_code, status.HTTP_200_OK)
        self.assertFalse(removed.data["is_endorsed"])
        self.assertEqual(removed.data["endorse_count"], 0)
        self.assertFalse(self.skill.endorsed_by.exists())
