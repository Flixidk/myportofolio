from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Experience, Skill
from main.forms import ExperienceForm, SkillForm


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

    def test_skill_page_renders_category_filters_and_api_endpoint(self):
        response = self.client.get(reverse("main:show_skill"), {"cat": "backend"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, 'data-category="backend"')
        self.assertContains(response, reverse("api:skill-list"))
        self.assertNotContains(response, self.skill.title)

    def test_models_have_readable_names(self):
        self.assertEqual(str(self.experience), "Event Staff")
        self.assertEqual(str(self.skill), "Python")

    def test_experience_ongoing_property(self):
        ongoing = Experience(title="Current Role", description="Still working", ended_at=None)
        self.assertTrue(ongoing.is_ongoing)
        self.assertFalse(self.experience.is_ongoing)


class AuthenticationPageTests(TestCase):
    def test_register_page_and_successful_registration(self):
        register_url = reverse("main:register")
        self.assertEqual(self.client.get(register_url).status_code, 200)

        response = self.client.post(register_url, {
            "username": "newstudent",
            "password1": "A-strong-test-password-839!",
            "password2": "A-strong-test-password-839!",
        })
        self.assertRedirects(response, reverse("main:login"))
        self.assertTrue(User.objects.filter(username="newstudent").exists())

    def test_invalid_registration_renders_errors(self):
        response = self.client.post(reverse("main:register"), {
            "username": "newstudent",
            "password1": "A-strong-test-password-839!",
            "password2": "different-password",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "register.html")
        self.assertContains(response, "password")
        self.assertFalse(User.objects.filter(username="newstudent").exists())

    def test_login_page_successful_login_and_logout(self):
        user = User.objects.create_user(username="returning", password="A-strong-test-password-839!")
        login_url = reverse("main:login")
        self.assertEqual(self.client.get(login_url).status_code, 200)

        response = self.client.post(login_url, {
            "username": "returning",
            "password": "A-strong-test-password-839!",
        })
        self.assertRedirects(response, reverse("main:show_main"))
        self.assertIn("last_login", response.cookies)

        logout_response = self.client.get(reverse("main:logout"))
        self.assertRedirects(logout_response, reverse("main:show_main"))
        self.assertEqual(logout_response.cookies["last_login"].value, "")

    def test_invalid_login_renders_login_form(self):
        response = self.client.post(reverse("main:login"), {
            "username": "missing-user",
            "password": "wrong-password",
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")


class FormCleaningTests(TestCase):
    def test_experience_form_strips_html_from_title_and_description(self):
        form = ExperienceForm(data={
            "title": " <b>Research Assistant</b> ",
            "description": " <p>Built a <strong>prototype</strong>.</p> ",
            "category": "research",
            "started_at": "2025-01-01",
            "ended_at": "2025-06-01",
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Research Assistant")
        self.assertEqual(form.cleaned_data["description"], "Built a prototype.")

    def test_experience_form_rejects_title_containing_only_html(self):
        form = ExperienceForm(data={
            "title": "<b></b>", "description": "Description", "category": "research",
            "started_at": "2025-01-01", "ended_at": "2025-06-01",
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_skill_form_cleans_title_description_and_icon_path(self):
        form = SkillForm(data={
            "title": " <b>Django</b> ", "category": "backend",
            "description": " <p>Web framework</p> ",
            "icon_path": " <b>https://example.com/django.svg</b> ", "order": 1,
        })
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["title"], "Django")
        self.assertEqual(form.cleaned_data["description"], "Web framework")
        self.assertEqual(form.cleaned_data["icon_path"], "https://example.com/django.svg")

    def test_skill_form_rejects_title_containing_only_html(self):
        form = SkillForm(data={
            "title": "<b></b>", "category": "backend", "description": "Description",
            "icon_path": "", "order": 1,
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


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
