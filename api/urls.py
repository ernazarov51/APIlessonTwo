"""
URL configuration for DRFp26 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView


from api import views

urlpatterns = [
    # path('hello/',views.DRF.as_view(),name='hello'),
    # path('greet/',views.DRF2.as_view(),name='sad'),

# ===================== Blog Views Full ================================

    # path('posts',views.posts_view),
    # path('add-post',views.add_post_view),
    # path('update-post/<int:pk>',views.update_post_view),
    # path('delete-post/<int:pk>',views.delete_post_view),
]

name='post'
urlpatterns += [
    path('post-list',views.posts_list_view),
    path('cretate-post',views.create_post_view),
    path('get-subjob',views.get_subjob_view),
    path('get-post2',views.get_post_view),
path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# HomeWork
urlpatterns += [
    path('task1',views.task1),
    path('task2',views.task2),
    path('task3',views.task3),
    path('task4',views.task4),
]