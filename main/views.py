import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required  
from django.core.exceptions import PermissionDenied        
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from main.models import Experience
from main.models import Skill
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

    context = {
        "name": "Nanta",
        "title_query" : title_query,
        "form": ExperienceForm(),
    }
    return render(request, "experience.html", context)

@login_required(login_url="/login/")
@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan pengalaman."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        experience = form.save()
        return JsonResponse(
            {"message": "Pengalaman berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

@login_required(login_url="/login/")
@permission_required("main.change_experience", raise_exception=True)
@require_POST
def edit_experience_ajax(request, experience_id):
    experience = get_object_or_404(Experience, id=experience_id)
    form = ExperienceForm(request.POST, instance=experience)
    
    if form.is_valid():
        form.save()
        return JsonResponse({"message": "Pengalaman berhasil diperbarui."}, status=200)

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def get_experience_json(request):
    title_query = request.GET.get("title", "").strip()
    experience_list = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experience_list = experience_list.filter(title__icontains=title_query)

    data = []
    for experience in experience_list:
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(experience.id),
            "fields": {
                "title": experience.title,
                "description": experience.description,
                "category" : experience.category,
                "category_display": experience.get_category_display(),
                "started_at" : str(experience.started_at) if experience.started_at else None,
                "ended_at" : str(experience.ended_at),
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

@login_required(login_url="/login/")
def toggle_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

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
    }
    return render(request, "skill.html", context)

@login_required(login_url="/login/")
@require_POST
def create_skill_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan skill."},
            status=403,
        )

    form = SkillForm(request.POST)
    if form.is_valid():
        skill = form.save()
        return JsonResponse(
            {"message": "Skill berhasil ditambahkan.", "pk": str(skill.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

def get_skill_json(request):
    selected_category = request.GET.get('cat', 'all')
    skills_list = Skill.objects.prefetch_related('endorsed_by').all()

    # Filter by category
    if selected_category and selected_category != 'all':
        skills_list = [s for s in skills_list if getattr(s, 'category', None) == selected_category]

    data = []
    for skill in skills_list:
        endorsed_users = skill.endorsed_by.all()
        is_endorsed = request.user in endorsed_users if request.user.is_authenticated else False
        endorsed_by_names = ", ".join([u.username for u in endorsed_users])

        data.append({
            "pk": str(skill.id),
            "fields": {
                "title": skill.title,
                "description": skill.description,
                "category": skill.get_category_display(),
                "icon_path" : skill.icon_path,
                "endorse_count": endorsed_users.count(),
                "is_endorsed": is_endorsed,
                "endorsed_by_names": endorsed_by_names,
            }
        })

    return JsonResponse(data, safe=False)

@login_required(login_url='/login/')
def delete_skill(request, skill_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill berhasil dihapus!")
        return redirect("main:show_skill")

    return redirect("main:show_skill")

@login_required(login_url="/login/")
def toggle_endorsement(request, skill_id):
    skill = get_object_or_404(Skill, pk=skill_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi endorsement, batalkan endorsement-nya.
        # Kalau belum, tambahkan endorsement
        if request.user in skill.endorsed_by.all():
            skill.endorsed_by.remove(request.user)
        else:
            skill.endorsed_by.add(request.user)

    return redirect("main:show_skill")