from django.contrib import admin
from django.urls import path
from LITRevu import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/',views.hello),


    # path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    # path('contact/', views.contact, name='contact'),
    # path('faq/', views.faq, name='faq'),
    # path('terms/', views.terms, name='terms'),
]
