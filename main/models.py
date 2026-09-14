from django.db import models

# Create your models here.
import uuid
from django.db import models

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        ) 
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_CHOICES, 
        default='full-time'
        )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return self.title   
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Dev Tools'),
    ]

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
        )
    title = models.CharField(max_length=255)
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='tools'
        )   
    description = models.TextField(blank=True, null=True)
    icon_path = models.CharField(
        max_length=100, 
        blank=True, 
        help_text ="icon (svg link) from devicon.dev")
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Lower numbers display first"
        )

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title