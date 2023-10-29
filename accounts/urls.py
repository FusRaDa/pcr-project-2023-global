from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .decorators import manager_only
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.accounts, name="accounts"),
    path("assign_role/<str:pk>/", views.assignUserRoles, name="roles"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name='profile'),
    path("activate/<uidb64>/<token>", views.activate, name='activate'),
    path("view/<str:username>/", views.view, name='view'),

    # Limit this page to only be accessible to Manager Group
    path('reset_password/', 
         login_required(manager_only(auth_views.PasswordResetView.as_view(template_name="password_reset.html"))), 
         name="reset_password"),

    path('reset_password_sent/', 
         login_required(manager_only(auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"))), 
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
         name="password_reset_confirm"),

    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
         name="password_reset_complete"),

]