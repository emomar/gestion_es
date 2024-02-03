from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .forms import SortieCreateForm, EnregistrementcreateForm
from .models import Sortie, Enregistrement

class EnregistrementCreateAdmin(admin.ModelAdmin):
    list_display = ['EnregistrementId', 'nom', 'prenom', 'numero_telephone', 'Date_heure_entree', 'lieu_visite', 'numero_badge','type_piece_identite','reference_piece', 'motif_visite','societe','photo']
    form = EnregistrementcreateForm

class SortieCreateAdmin(admin.ModelAdmin):
    list_display = ['enregistrement_info', 'Date_heure_sortie']
    form = SortieCreateForm
    
    def enregistrement_info(self, obj):
        return f"Sortie de {obj.enregistrement.nom} {obj.enregistrement.prenom} ({obj.enregistrement.reference_piece}) à {obj.Date_heure_sortie}. EnregistrementId: {obj.enregistrement.EnregistrementId}, Numéro de téléphone: {obj.enregistrement.numero_telephone}, Numéro de badge: {obj.enregistrement.numero_badge}"

    enregistrement_info.short_description = 'Enregistrement'

# Enregistrement des modèles dans le panneau d'administration
admin.site.register(Sortie, SortieCreateAdmin)
admin.site.register(Enregistrement, EnregistrementCreateAdmin)
