from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views

from core.views import HomePageView


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'accounts/login/', views.login, name='auth_login'),
    url(r'accounts/logout/', views.logout, name='auth_logout'),
    url(r'^$', HomePageView.as_view(), name="index"),
]
