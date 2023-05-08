from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import MainView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('download/', MainView.download_file, name='download'),
    path('insert/'  , MainView.insert       , name='insert'),
    path('delete/'  , MainView.delete       , name='delete'),
    path('login/'   , MainView.login_view   , name='login'),
    path('logout/'  , MainView.logout_view  , name='logout'),
]