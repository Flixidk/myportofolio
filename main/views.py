import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied        
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from main.models import Skill
from main.permissions import user_is_editor
from .forms import ExperienceForm, SkillForm

''' =============================
    Functions for Authentication
    ============================= '''
def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Nanta",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Nanta",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response;

''' =============================== 
    Functions for Main Landing Page
    =============================== '''
def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Nanta",
        "full_name" : "Muhammad Raihananta Adzaky Yuwono",
        "npm": "2506547853",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "CS student at the University of Indonesia. I'm very eager to grow my skills in programming, software development and cybersecurity."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)

''' =============================
    Functions for Experience Page
    ============================= '''
def show_experience(request):
    title_query = request.GET.get("title", "").strip()
    can_edit_experience = request.user.is_superuser or user_is_editor(request.user)

    context = {
        "name": "Nanta",
        "title_query" : title_query,
        "can_edit_experience": can_edit_experience,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

''' =========================
    Functions for Skill Page
    ========================= '''
def show_skill(request):
    selected_category = request.GET.get('cat', 'all')

    categories = [
        ('all', 'All'),
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('database', 'Database'),
        ('tools', 'Dev Tools'),
    ]

    context = {
        "name": "Nanta",
        "categories" : categories,
        'selected_category' : selected_category,
        "form": SkillForm(),
        "can_edit_skill": request.user.is_superuser or user_is_editor(request.user),
    }
    return render(request, "skill.html", context)