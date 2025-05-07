from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app.views import toggle_warning



urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('links/', views.links, name='links'),
    path("feedback/", views.feedback, name="feedback"),
    path("pool/", views.feedback, name="pool"),
    #админка
    #регистрация
    path('registration/', views.registration, name='registration'),
    #блог
    path('blog/', views.blog, name='blog'),
    path('blog/<int:parametr>/', views.blogpost, name='blogpost'),
    path('blog/newpost/', views.newpost, name='newpost'),
    path('video/', views.videopost, name='videopost'),
    path('toggle-warning/<int:branch_id>/', toggle_warning, name='toggle_warning'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
