from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register, name="register"),
    path("welcome/", views.welcome, name="welcome"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("records/", views.records, name="records"),

    # path("add_record/", views.add_record, name="add_record"),
]
