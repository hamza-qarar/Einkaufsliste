"""
URL configuration for Einkaufsliste project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView, LogoutView
from mylist.views import mylist, delete_item, edit_item, toggle_item, create_list, events, delete_event, notes, delete_note, register

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('register/', register, name='register'),
    path('admin/', admin.site.urls),
    path('mylist/', mylist),
    path('mylist/delete/<int:item_id>/', delete_item),
    path('mylist/toggle/<int:item_id>/', toggle_item),
    path('mylist/edit/<int:item_id>/', edit_item),
    path('mylist/create-list/', create_list),
    path('mylist/events/', events),
    path('mylist/events/delete/<int:event_id>/', delete_event),
    path('mylist/notes/', notes),
    path('mylist/notes/delete/<int:note_id>/', delete_note),
]
