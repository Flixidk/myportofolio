from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput, Select, NumberInput

from main.models import Experience, Skill

EXPERIENCE_CHOICES = [
    ('internship', 'Internship'),
    ('research', 'Research'),
    ('volunteer', 'Volunteer'),
    ('part-time', 'Part-Time'),
    ('full-time', 'Full-Time'),
    ('freelance', 'Freelance'),
]

class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Pengalaman",
            "description": "Deskripsi Pengalaman",
            "category": "Jenis Pengalaman",
            "started_at": "Start Date",
            "ended_at": "End Date",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Staff Event",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "rows": 3,
                }
            ),
            "category": Select(
                choices=EXPERIENCE_CHOICES,
            ),
            "started_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date",
                }
            ),
        }

SKILL_CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Dev Tools'),
    ]

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = [
            "title",
            "category",
            "description",
            "icon_path",
            "order",
        ]

        labels = {
            "title" : "Nama Skill",
            "category" : "Kategori",
            "description" : "Deskripsi Skill",
            "icon_path" : "Devicon Path",
            "order" : "Urutan",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Java",
                    "maxlength": 255,
                }
            ),
            "category": Select(
                            choices=SKILL_CATEGORY_CHOICES,
                        ),
            "description": TextInput(
                attrs={
                    "placeholder": "Ceritakan Pengalamanmu",
                    "maxlength" : 255,
                }
            ),
            "icon_path" : URLInput(
                attrs={
                    "placeholder": "https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/...",
                    "maxlength" : 255,
                }
            ),
            "order" : NumberInput(
                attrs={
                    "placeholder" : "Input Ordering Number",
                }
            )   
        }

