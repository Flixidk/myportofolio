from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.models import Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Event Staff DDP0",
            description="Membantu menjalankan acara",
            category="part-time",
            started_at=timezone.make_aware(datetime(2026, 4, 1, 0, 0)),
            ended_at=timezone.make_aware(datetime(2026, 4, 22, 0, 0))
        )

        self.skill = Skill.objects.create(
            title="Python",
            category="backend",
            description="Basic Syntaxing",
            icon_path="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg"
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
    