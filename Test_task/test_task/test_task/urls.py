"""test_task URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from test_task_poll_app import views

urlpatterns = [
    path('<int:user_id>/results/', views.results, name='results'),
    path('<int:user_id>/results_main', views.results_main, name='results_main'),
    path('<int:user_id>/vote/submit/<int:poll_id>', views.submit, name='submit'),
    path('<int:user_id>/', views.home, name='home'),
    path('<int:user_id>/vote/', views.vote, name='vote'),
    path('admin/', admin.site.urls),
]
