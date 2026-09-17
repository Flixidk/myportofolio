from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse

from main.models import Experience
from main.models import Skill
from .forms import ExperienceForm, SkillForm

''' ===============================
    Functions for Main Landing Page
    =============================== '''
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

''' =============================
    Functions for Experience Page
    ============================= '''
def show_experience(request):
    json_response = get_experience_json(request)

    experience_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [experience.object for experience in experience_data]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Nanta",
        "experience_list": experience_list,
        "title_query" : title_query,
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

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience_list = Experience.objects.all()

    if title_query:
        experience_list = experience_list.filter(title__icontains=title_query)

    experience_json = serializers.serialize("json", experience_list)
    return HttpResponse(experience_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

''' =========================
    Functions for Skill Page
    ========================= '''
def show_skill(request):
    selected_category = request.GET.get('cat', 'all')

    # Fetch and deserialize JSON data
    json_response = get_skill_json(request)
    skill_data = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    skills_list = [skill.object for skill in skill_data]

    # Filter by category
    if selected_category and selected_category != 'all':
        skills_list = [s for s in skills_list if getattr(s, 'category', None) == selected_category]

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

def create_skill(request):
    form = SkillForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Skill baru berhasil ditambahkan!")
        return redirect("main:show_skill")

    context = {
        "name": "Nanta",
        "form": form,
    }
    return render(request, "skill_form.html", context)

def get_skill_json(request):
    title_query = request.GET.get("title", "").strip()
    skill_list = Skill.objects.all()

    if title_query:
        skill_list = skill_list.filter(title__icontains=title_query)

    skill_json = serializers.serialize("json", skill_list)
    return HttpResponse(skill_json, content_type="application/json")

def delete_skill(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")