from django.forms import ModelForm, TextInput, Textarea, URLInput, DateInput, Select

from main.models import Experience

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