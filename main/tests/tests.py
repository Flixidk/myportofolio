import json
from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Skill


class PortfolioPageTests(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Event Staff",
            description="Helped run an event",
            category="part-time",
            started_at=date(2026, 4, 1),
            ended_at=date(2026, 4, 22),
        )
        self.skill = Skill.objects.create(
            title="Python",
            category="backend",
            description="Basic syntax",
            icon_path="https://example.com/python.svg",
        )

    def test_unknown_page_returns_404(self):
        self.assertEqual(self.client.get("/page-that-does-not-exist/").status_code, 404)

    def test_landing_page_renders_navigation(self):
        response = self.client.get(reverse("main:show_main"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, reverse("main:show_experience"))
        self.assertContains(response, reverse("main:show_skill"))

    def test_experience_page_renders_search_and_api_endpoint(self):
        response = self.client.get(reverse("main:show_experience"), {"title": " Event "})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, 'value="Event"')
        self.assertContains(response, reverse("api:experience-list"))
        self.assertNotContains(response, self.experience.title)

    def test_skill_page_renders_category_filters_and_json_endpoint(self):
        response = self.client.get(reverse("main:show_skill"), {"cat": "backend"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, 'data-category="backend"')
        self.assertContains(response, reverse("main:get_skill_json"))
        self.assertNotContains(response, self.skill.title)

    def test_models_have_readable_names(self):
        self.assertEqual(str(self.experience), "Event Staff")
        self.assertEqual(str(self.skill), "Python")


class SkillEndpointTests(TestCase):
    def setUp(self):
        self.skill = Skill.objects.create(
            title="Python", category="backend", description="Basic syntax", order=1
        )
        self.other_skill = Skill.objects.create(
            title="HTML", category="frontend", description="Markup", order=2
        )

    def test_skill_json_returns_current_payload(self):
        response = self.client.get(reverse("main:get_skill_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual([item["fields"]["title"] for item in data], ["Python", "HTML"])
        self.assertEqual(data[0]["fields"]["category"], "Backend")
        self.assertEqual(data[0]["fields"]["endorse_count"], 0)
        self.assertFalse(data[0]["fields"]["is_endorsed"])

    def test_skill_json_filters_by_category(self):
        response = self.client.get(reverse("main:get_skill_json"), {"cat": "backend"})
        data = json.loads(response.content)
        self.assertEqual([item["fields"]["title"] for item in data], ["Python"])

    def test_skill_json_includes_endorsement_state_for_signed_in_user(self):
        user = User.objects.create_user(username="student", password="password")
        self.skill.endorsed_by.add(user)
        self.client.force_login(user)
        data = json.loads(self.client.get(reverse("main:get_skill_json")).content)
        self.assertEqual(data[0]["fields"]["endorsed_by_names"], "student")
        self.assertTrue(data[0]["fields"]["is_endorsed"])

    def test_skill_creation_requires_superuser_and_valid_payload(self):
        url = reverse("main:create_skill_ajax")
        payload = {"title": "Django", "category": "backend", "description": "Framework", "icon_path": "", "order": 0}

        self.assertEqual(self.client.post(url, payload).status_code, 302)
        regular_user = User.objects.create_user(username="student", password="password")
        self.client.force_login(regular_user)
        self.assertEqual(self.client.post(url, payload).status_code, 403)
        owner = User.objects.create_superuser(username="owner", email="owner@example.com", password="password")
        self.client.force_login(owner)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Skill.objects.filter(title="Django").exists())
        self.assertIn("pk", json.loads(response.content))

    def test_skill_creation_rejects_invalid_payload(self):
        owner = User.objects.create_superuser(username="owner", email="owner@example.com", password="password")
        self.client.force_login(owner)
        response = self.client.post(reverse("main:create_skill_ajax"), {"title": "<b></b>"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("errors", json.loads(response.content))

    def test_endorsement_toggles_for_authenticated_user(self):
        user = User.objects.create_user(username="student", password="password")
        url = reverse("main:toggle_endorsement", kwargs={"skill_id": self.skill.pk})
        self.assertEqual(self.client.post(url).status_code, 302)
        self.client.force_login(user)
        self.client.post(url)
        self.assertTrue(self.skill.endorsed_by.filter(pk=user.pk).exists())
        self.client.post(url)
        self.assertFalse(self.skill.endorsed_by.filter(pk=user.pk).exists())

    def test_delete_skill_is_owner_only_and_post_only(self):
        url = reverse("main:delete_skill", kwargs={"skill_id": self.skill.pk})
        self.assertEqual(self.client.get(url).status_code, 302)
        user = User.objects.create_user(username="student", password="password")
        self.client.force_login(user)
        self.assertEqual(self.client.post(url).status_code, 403)
        owner = User.objects.create_superuser(username="owner", email="owner@example.com", password="password")
        self.client.force_login(owner)
        self.assertEqual(self.client.get(url).status_code, 302)
        self.assertTrue(Skill.objects.filter(pk=self.skill.pk).exists())
        self.client.post(url)
        self.assertFalse(Skill.objects.filter(pk=self.skill.pk).exists())


class ExperienceApiTests(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Event Staff", description="Helped run an event", category="part-time",
            started_at=date(2026, 4, 1), ended_at=date(2026, 4, 22),
        )
        self.list_url = reverse("api:experience-list")
        self.detail_url = reverse("api:experience-detail", kwargs={"experience_id": self.experience.pk})

    def test_list_and_title_filter_are_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], "Event Staff")
        filtered = self.client.get(self.list_url, {"title": "event"})
        self.assertEqual(len(filtered.json()), 1)
        self.assertEqual(len(self.client.get(self.list_url, {"title": "missing"}).json()), 0)

    def test_detail_returns_serialized_experience(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["category"], "part-time")
        self.assertEqual(response.json()["star_count"], 0)

    def test_writes_require_portfolio_owner(self):
        payload = {
            "title": "<b>Developer</b>", "description": "<p>Build APIs</p>",
            "category": "full-time", "started_at": "2026-05-01", "ended_at": "2026-09-01",
        }
        self.assertEqual(self.client.post(self.list_url, payload, content_type="application/json").status_code, 403)
        owner = User.objects.create_superuser(username="owner", email="owner@example.com", password="password")
        self.client.force_login(owner)
        created = self.client.post(self.list_url, payload, content_type="application/json")
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["title"], "Developer")
        self.assertEqual(created.json()["description"], "Build APIs")

    def test_owner_can_patch_and_delete(self):
        owner = User.objects.create_superuser(username="owner", email="owner@example.com", password="password")
        self.client.force_login(owner)
        updated = self.client.patch(self.detail_url, {"title": "Updated"}, content_type="application/json")
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.json()["title"], "Updated")
        deleted = self.client.delete(self.detail_url)
        self.assertEqual(deleted.status_code, 204)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_authenticated_user_can_toggle_star(self):
        user = User.objects.create_user(username="student", password="password")
        url = reverse("api:experience-star", kwargs={"experience_id": self.experience.pk})
        self.assertEqual(self.client.post(url).status_code, 403)
        self.client.force_login(user)
        first = self.client.post(url)
        self.assertEqual(first.status_code, 200)
        self.assertTrue(first.json()["is_starred"])
        self.assertEqual(first.json()["star_count"], 1)
        second = self.client.post(url)
        self.assertFalse(second.json()["is_starred"])
        self.assertEqual(second.json()["star_count"], 0)
