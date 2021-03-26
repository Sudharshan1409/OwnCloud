from django.urls import path
from . import views
app_name = 'cloud'

urlpatterns = [
    path('',views.CloudHomePage.as_view(),name = 'home'),
    path('<int:pk>/',views.CloudFolderPage.as_view(),name = 'folder'),
    path('file/',views.AddFileAPI.as_view(),name = 'file_api'),
    path('delete/',views.DeleteAPI.as_view(),name = 'delete'),
    path('folder/',views.AddFolderAPI.as_view(),name = 'folder_api'),
]
