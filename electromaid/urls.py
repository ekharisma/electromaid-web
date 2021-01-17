from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.Contact.as_view(), name='contact'),
    path('blog/', views.blog, name='blog'),
    # path('blog/<int:id>/', views.blog_id, name='blog_id'),
    path('learnmore/', views.learn_more, name='learn_more'),
    path('login/', views.Login_view.as_view(), name='login'),
    path('register/', views.Register_view.as_view(), name='register'),
    path('dashboard/control/', views.Control_view.as_view(), name='control'),
    path('dashboard/usage', views.Usage.as_view(), name='usage'),
    path('dashboard/logout', views.logout, name='logout'),
]