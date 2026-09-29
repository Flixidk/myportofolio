from django.urls import path

from main.views import *

app_name = "main"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("", show_main, name="show_main"),
    
    
    path("experience/", show_experience, name="show_experience"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path('experience/<uuid:experience_id>/edit-ajax/', edit_experience_ajax, name='edit_experience_ajax'),
    path("experience/<uuid:experience_id>/delete/",delete_experience,name="delete_experience"),
    path("api/experience", get_experience_json, name="get_experience_json"),
    path("projects/<uuid:experience_id>/star/", toggle_star, name="toggle_star",),

    path("skill/", show_skill, name="show_skill"),
    path("skill/add-ajax/", create_skill_ajax, name="create_skill_ajax"),
    path("api/skill", get_skill_json, name="get_skill_json"),
    path("skill/<uuid:skill_id>/delete/",delete_skill, name="delete_skill"),
    path("skill/<uuid:skill_id>/endorse/", toggle_endorsement, name="toggle_endorsement",),
]