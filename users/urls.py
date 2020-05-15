from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
app_name = 'users'

urlpatterns = [
    path('',views.UserHomePage.as_view(),name = 'home'),
    path('signup/',views.RegisterUserPage.as_view(),name = 'register'),
    path('login/',LoginView.as_view(template_name = 'users/login.html'), name="login"),
    path('logout/',LogoutView.as_view(next_page = '/'),name = 'logout',kwargs = {'next_page':'/'}),
    path('update/<int:pk>',views.UpdateUserPage.as_view(),name = 'update'),
]
