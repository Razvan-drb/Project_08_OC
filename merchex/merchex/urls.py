from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from LITRevu import views

urlpatterns = [
    path('', RedirectView.as_view(url='/home', permanent=False)),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('flux/', views.flux, name='flux'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('manage_followers/', views.manage_followers, name='manage_followers'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('create-critique/', views.create_critique, name='create_critique'),
    path('hide-critique/<int:critique_id>/', views.hide_critique, name='hide_critique'),
    path('hide_ticket/<int:ticket_id>/', views.hide_ticket, name='hide_ticket'),

    # see static for urls Django
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# condition ou la valeur debug dans setting is True

