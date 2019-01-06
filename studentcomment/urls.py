from django.contrib import admin
from django.urls import path,include
from studentcomment import views
admin.autodiscover()

urlpatterns = [
    path('', views.edit),
    path('error/',views.error),
    path('test/',views.test)
]