from django.urls import path
from . import views
app_name = 'cloud'

urlpatterns = [
    path('',views.CloudHomePage.as_view(),name = 'home'),
    path('<int:pk>/',views.CloudFolderPage.as_view(),name = 'folder'),
    path('add_file/',views.AddFileAPI.as_view(),name = 'add_file'),
    path('add_folder/',views.AddFolderAPI.as_view(),name = 'add_folder'),
]
