from django.urls import path
from django.contrib import admin
from Emomar import views
from django.conf import settings
from .views import HomeView
from django.conf.urls.static import static
from .views import ListeVisiteur_jourView
from Emomar.views import InformationsSupplementairesView

urlpatterns = [
    path('', views.Login, name='login-page'),
    path('accounts/register/', views.Register, name='register-page'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('home/', HomeView.as_view(), name='home'),
    path('Ajouter_visiteur/', views.AjouterVisiteurView.as_view(), name='Ajouter_visiteur'),
    path('Ajouter_sortie/', views.Ajouter_sortieView.as_view(), name='Ajouter_sortie'),
    path('table/liste_visiteur/',views. ListeVisiteurView.as_view(), name='liste_visiteur'),
    path('table/modifier_enregistrement/<int:enregistrement_id>/',views. ModifierEnregistrementView.as_view(), name='modifier_enregistrement'),
    path('liste_sortie/', views.ExitpageView.as_view(),name='liste_sortie'),
    path('liste_visiteur_jour/', ListeVisiteur_jourView.as_view(), name='liste_visiteur_jour'),
    path('informations_supplementaires/<int:pk>/', InformationsSupplementairesView.as_view(), name='informations_supplementaires'),
    
    path('admin/', admin.site.urls)

##layouts

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
