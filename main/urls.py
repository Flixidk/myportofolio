from django.urls import path

from main.views import show_main, show_experience, show_skill, create_experience, get_experience_json, delete_experience, create_skill, get_skill_json

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("skill/", show_skill, name="show_skill"),
    path("experience/add/", create_experience, name="create_experience"),
    path("experience/<uuid:experience_id>/delete/",delete_experience,name="delete_experience"),
    path("api/experience", get_experience_json, name="get_experience_json"),
    path("skill/add/", create_skill, name="create_skill"),
    path("api/skill", get_skill_json, name="get_skill_json"),
]