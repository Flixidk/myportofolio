from django.shortcuts import render

# Create your views here.
from main.models import Experience

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