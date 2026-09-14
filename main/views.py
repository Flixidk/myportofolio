from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

from main.models import Experience
from main.models import Skill
from .forms import ExperienceForm

def show_main(request):
    context = {
        "name": "Nanta",
        "full_name" : "Muhammad Raihananta Adzaky Yuwono",
        "npm": "2506547853",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at the University of Indonesia. I'm very eager to grow my skills in programming, software development and cybersecurity."
        ),
    }
    return render(request, "index.html", context)

def show_experience(request):
    context = {
        "name": "Nanta",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman baru berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Nanta",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def show_skill(request):
    selected_category = request.GET.get('cat', 'all')

    # Filter based on category
    if selected_category and selected_category != 'all':
        skills_list = Skill.objects.filter(category=selected_category)
    else:
        skills_list = Skill.objects.all()

    categories = [
        ('all', 'All'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Dev Tools'),
    ]

    context = {
        "name" : "Nanta",
        "skills_list" : skills_list,
        "categories" : categories,
        'selected_category' : selected_category,
    }
    return render(request, "skill.html", context)