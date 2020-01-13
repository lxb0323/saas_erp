from django.contrib import admin
from django.urls import path, re_path
from db_module import views as v

urlpatterns = [
    re_path('^create_unit/$',v.CreateUnit.as_view()),
    re_path('^create_material/$',v.CreateRawMaterial.as_view()),
    re_path('^create_merchant/$',v.CreateMerchant.as_view()),
]
