import json
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Event Staff DDP0",
            description="Membantu menjalankan acara",
            category="part-time",
            started_at=timezone.make_aware(datetime(2026, 4, 1, 0, 0)),
            ended_at=timezone.make_aware(datetime(2026, 4, 22, 0, 0)),
        )

        self.skill = Skill.objects.create(
            title="Python",
            category="backend",
            description="Basic Syntaxing",
            icon_path="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg",
        )

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")
        self.assertEqual(response.status_code, 404)

    def test_landing_page(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_skill")}"')

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No stations built yet.")

    def test_skill_page(self):
        response = self.client.get(reverse("main:show_skill"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill.html")
        self.assertContains(response, self.skill.title)
        self.assertContains(response, self.skill.description)

    def test_empty_skill_page(self):
        Skill.objects.all().delete()
        response = self.client.get(reverse("main:show_skill"))

        self.assertContains(response, "No Skills Found")

    def test_skill_category_filtering(self):
        response = self.client.get(reverse("main:show_skill") + "?cat=backend")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.skill.title)

        response_empty = self.client.get(reverse("main:show_skill") + "?cat=frontend")

        self.assertEqual(response_empty.status_code, 200)
        self.assertNotContains(response_empty, self.skill.title)
        self.assertContains(response_empty, "No Skills Found")

    def test_experience_model_str(self):
        self.assertEqual(str(self.experience), "Event Staff DDP0")

    def test_skill_model_str(self):
        self.assertEqual(str(self.skill), "Python")

    # --- Integrated Experience CRUD & Endpoint Tests ---

    def test_create_experience_get(self):
        response = self.client.get(reverse("main:create_experience"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertFalse(response.context["is_edit"])

    def test_create_experience_post_success(self):
        payload = {
            "title": "Backend Developer",
            "description": "Building APIs",
            "category": "full-time",
            "started_at": "2026-05-01",
            "ended_at": "2026-09-01",
        }
        response = self.client.post(reverse("main:create_experience"), data=payload)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertTrue(Experience.objects.filter(title="Backend Developer").exists())

    def test_edit_experience_get(self):
        url = reverse("main:edit_experience", kwargs={"experience_id": self.experience.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience_form.html")
        self.assertTrue(response.context["is_edit"])

    def test_edit_experience_post_success(self):
        url = reverse("main:edit_experience", kwargs={"experience_id": self.experience.id})
        payload = {
            "title": "Updated Event Staff",
            "description": self.experience.description,
            "category": self.experience.category,
            "started_at": "2026-04-01",
            "ended_at": "2026-04-22",
        }
        response = self.client.post(url, data=payload)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Updated Event Staff")

    def test_get_experience_json(self):
        response = self.client.get(reverse("main:get_experience_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_get_experience_json_filtering(self):
        # Covers: if title_query: branch when title param matches
        response = self.client.get(reverse("main:get_experience_json"), {"title": "Event"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        # Query that returns no results
        response_empty = self.client.get(reverse("main:get_experience_json"), {"title": "Nonexistent"})
        self.assertEqual(response_empty.status_code, 200)
        data_empty = json.loads(response_empty.content)
        self.assertEqual(len(data_empty), 0)

    def test_delete_experience_get_redirects(self):
        # Covers: bottom `return redirect("main:show_experience")` when method is GET
        url = reverse("main:delete_experience", kwargs={"experience_id": self.experience.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("main:show_experience"))
        # Verify the object was NOT deleted
        self.assertTrue(Experience.objects.filter(id=self.experience.id).exists())

    def test_delete_experience_post(self):
        url = reverse("main:delete_experience", kwargs={"experience_id": self.experience.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("main:show_experience"))
        self.assertFalse(Experience.objects.filter(id=self.experience.id).exists())

    # --- Integrated Skill CRUD & Endpoint Tests ---

    def test_create_skill_get(self):
        response = self.client.get(reverse("main:create_skill"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "skill_form.html")

    def test_create_skill_post_success(self):
        payload = {
            "title": "Django",
            "category": "backend",
            "description": "Web Framework",
            "icon_path": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg",
            "order": 0,
        }
        response = self.client.post(reverse("main:create_skill"), data=payload)
        self.assertRedirects(response, reverse("main:show_skill"))
        self.assertTrue(Skill.objects.filter(title="Django").exists())

    def test_get_skill_json(self):
        response = self.client.get(reverse("main:get_skill_json"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_get_skill_json_filtering(self):
        # Covers: skill_list = skill_list.filter(...)
        response = self.client.get(reverse("main:get_skill_json"), {"title": "Py"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

        # Query that returns no results
        response_empty = self.client.get(reverse("main:get_skill_json"), {"title": "Nonexistent"})
        self.assertEqual(response_empty.status_code, 200)
        data_empty = json.loads(response_empty.content)
        self.assertEqual(len(data_empty), 0)

    def test_delete_skill_get_redirects(self):
        # Covers: bottom `return redirect("main:show_skill")` when method is GET
        url = reverse("main:delete_skill", kwargs={"skill_id": self.skill.id})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("main:show_skill"))
        # Verify the object was NOT deleted
        self.assertTrue(Skill.objects.filter(id=self.skill.id).exists())

    def test_delete_skill_post(self):
        url = reverse("main:delete_skill", kwargs={"skill_id": self.skill.id})
        response = self.client.post(url)
        self.assertRedirects(response, reverse("main:show_skill"))
        self.assertFalse(Skill.objects.filter(id=self.skill.id).exists())