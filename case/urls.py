
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/',views.register),
    path('',views.Search),
    path('login/',views.Signin),
    path('dashboard/',views.dashboard),
    path('register_case/',views.register_case),
    path("logout/", views.Signout),
    path('find/',views.findperson)

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
