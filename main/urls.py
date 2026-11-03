from django.urls import include, path

from main.views import *

app_name = "main"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("", show_main, name="show_main"),    
    
    path("experience/", show_experience, name="show_experience"),
    path("skill/", show_skill, name="show_skill"),

    path("api/v1/", include("main.api_urls")),
    path("api-auth/", include("rest_framework.urls")),
]