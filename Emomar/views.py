from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Enregistrement,Sortie
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib import messages
from .models import Enregistrement,Sortie
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import  SortieCreateForm,EnregistrementcreateForm
from django.urls import reverse_lazy
from django.views.generic import RedirectView
import logging
from datetime import datetime 
from datetime import datetime, timedelta
from django.http import HttpResponseForbidden
import re
import calendar

# Create your views here.
@login_required

def Register(request):
    error_message = None

    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        name = request.POST.get('uname')
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # Validation du format du mot de passe
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            error_message = 'Le mot de passe doit contenir au moins 8 caractères avec des lettres et des chiffres.'
        else:
            try:
                new_user = User.objects.create_user(username=name, email=email, password=password)
                new_user.first_name = fname
                new_user.last_name = lname
                new_user.save()
                return redirect('login-page')
            except IntegrityError as e:
                print(f"Error: {e}")
                error_message = "Ce nom d'utilisateur est déjà utilisé. Veuillez en choisir un autre."

    return render(request, 'accounts/register.html', {'error_message': error_message})



def Login(request):
    error_message = None

    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('pass')

        # Vérification du format du mot de passe
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            error_message = 'Le mot de passe doit contenir au moins 8 caractères avec des lettres et des chiffres.'
        else:
            user = authenticate(request, username=name, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = 'Désolé, cet utilisateur n\'existe pas. Veuillez saisir vos informations correctement.'

    return render(request, 'accounts/login.html', {'error_message': error_message})


def logoutuser(request):
    logout(request)
    return redirect('login-page')


def test(request):
    return render(request, 'test.html', {})

class HomeView(View):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        current_date = timezone.now().date()

        # Calculer le début et la fin de l'année actuelle
        start_of_year = current_date.replace(month=1, day=1)
        end_of_year = current_date.replace(month=12, day=31)
        
        # Calculer le début et la fin de la semaine actuelle
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)

        current_date = timezone.now().date()

        # Requête pour le nombre total de sorties depuis le début de l'année
        total_exits = Sortie.objects.filter(Date_heure_sortie__date__range=[start_of_year, current_date]).count()

        # Compter le nombre de sorties par jour (en fonction de la date)
        exits_per_day = Sortie.objects.filter(Date_heure_sortie__date=current_date).count()

        # Requête pour le nombre total d'entrées depuis le début de l'année
        total_entries = Enregistrement.objects.filter(Date_heure_entree__date__range=[start_of_year, current_date]).count()

        # Compter le nombre d'entrées par jour (en fonction de la date)
        entries_per_day = Enregistrement.objects.filter(Date_heure_entree__date=current_date).count()
        
        start_of_week = current_date - timedelta(days=current_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        # Initialize a dictionary to store entries per day
        entries_per_days = {}
        exits_per_days = {}
        
        # Loop through each day of the week (Monday to Sunday)
        for day in range(7):
            # Calculate the start and end dates for the current day
            start_of_day = start_of_week + timedelta(days=day)
            end_of_day = start_of_day + timedelta(days=1)

            # Query the database for entries on the current day
            entries_count = Enregistrement.objects.filter(Date_heure_entree__date=start_of_day).count()
            exits_count = Sortie.objects.filter(Date_heure_sortie__date=start_of_day).count()

            # Store the entries count for the current day in the dictionary
            entries_per_days[start_of_day.strftime('%A')] = entries_count
            exits_per_days[start_of_day.strftime('%A')] = exits_count

        # Calculer le début et la fin du mois actuel
        start_of_month = current_date.replace(day=1)
        next_month = current_date.replace(day=28) + timedelta(days=4)
        end_of_month = next_month - timedelta(days=next_month.day)

        # Requête pour le nombre de sorties par mois
        exits_per_month = []
        entries_per_month = []
        months = []

        for month in range(1, 13):
            start_month = current_date.replace(month=month, day=1)
            end_month = start_month.replace(day=calendar.monthrange(start_month.year, start_month.month)[1])
            months.append(start_month.strftime("%b"))

            exits_per_month.append(Sortie.objects.filter(Date_heure_sortie__date__range=[start_month, end_month]).count())
            entries_per_month.append(Enregistrement.objects.filter(Date_heure_entree__date__range=[start_month, end_month]).count())

        # Requête pour le nombre d'entrées par semaine
        entries_per_week = Enregistrement.objects.filter(Date_heure_entree__date__range=[start_of_week, end_of_week]).count()

        # Requête pour le nombre de sorties par semaine
        exits_per_week = Sortie.objects.filter(Date_heure_sortie__date__range=[start_of_week, end_of_week]).count()

        context = {
            'parent': 'dashboard',
            'segment': 'dashboardv1',
            'total_entries': total_entries,
            'total_exits': total_exits,
            'entries_per_day': entries_per_day,
            'entries_per_days': entries_per_days,
            'exits_per_day': exits_per_day,
            'exits_per_days': exits_per_days,
            'entries_per_week': entries_per_week,
            'exits_per_week': exits_per_week,
            'entries_per_month': entries_per_month,
            'exits_per_month': exits_per_month,
            'months': months,
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
class ListeVisiteur_jourView(View):
    template_name = 'pages/tables/liste_visiteur_jour.html'

    def get(self, request, *args, **kwargs):
        today = datetime.now().date()

        # Filtrer les enregistrements pour la journée actuelle
        enregistrements = Enregistrement.objects.filter(Date_heure_entree__date=today).order_by('-Date_heure_entree')

        total_entries = enregistrements.count()

        context = {
            'enregistrements': enregistrements,
            'total_entries': total_entries,
        }

        return render(request, self.template_name, context)
logger = logging.getLogger(__name__)

class InformationsSupplementairesView(View):
    def get(self, request, pk):
        try:
            visiteur = get_object_or_404(Enregistrement, pk=pk)

            data = {
                'nom': visiteur.nom,
                'prenom': visiteur.prenom,
                'numero_telephone': visiteur.numero_telephone,
                'Date_heure_entree': visiteur.Date_heure_entree.strftime("%Y-%m-%d %H:%M:%S"),
                'lieu_visite': visiteur.lieu_visite,
                'numero_badge': visiteur.numero_badge,
                'reference_piece': visiteur.reference_piece,
                'motif_visite': visiteur.motif_visite,
                'societe': visiteur.societe,
                'type_piece_identite': visiteur.get_type_piece_identite_display(),
                'photo_url': visiteur.photo.url if visiteur.photo else None,
            }

            return JsonResponse(data)
        except Exception as e:
            logger.error(f"Erreur dans InformationsSupplementairesView: {e}")
            return JsonResponse({'error': 'Une erreur s\'est produite.'}, status=500)

class AjouterVisiteurView(View):
    template_name = 'pages/forms/Ajouter_visiteur.html'

    def get(self, request, *args, **kwargs):
        # Ajoutez ici le code pour obtenir le nombre total d'entrées
        total_entries = Enregistrement.objects.count()
        
        context = {
            'total_entries': total_entries
        }

        return render(request, self.template_name, context)
    @method_decorator(csrf_exempt)  # Assurez-vous d'importer csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.FILES)
        data = {
            'nom': request.POST.get('nom'),
            'prenom': request.POST.get('prenom'),
            'numero_telephone': request.POST.get('numero_telephone'),
            'Date_heure_entree': request.POST.get('Date_heure_entree'),
            'lieu_visite': request.POST.get('lieu_visite'),
            'numero_badge': request.POST.get('numero_badge'),
            'type_piece_identite': request.POST.get('type_piece_identite'),
            'reference_piece': request.POST.get('reference_piece'),
            'societe': request.POST.get('societe'),
            'motif_visite': request.POST.get('motif_visite'),
            'photo': request.FILES.get('photo'),
        }

        try:
            # Ajoutez ici la logique de validation des données, par exemple :
            if not data['nom'] or not data['prenom']:
                messages.error(request, "Veuillez remplir tous les champs obligatoires.")
                return render(request, self.template_name)

            # Enregistrez l'objet dans la base de données
            created = Enregistrement.objects.create(**data)

            # Comptez le nombre total d'entrées
            total_entries = Enregistrement.objects.count()

            if created:
                messages.success(request, f"Visiteur enregistré avec succès. Nombre total d'entrées : {total_entries}")
            else:
                messages.error(request, "Désolé, veuillez réessayer. Les données envoyées sont corrompues.")
        except Exception as e:
            messages.error(request, f"Désolé, notre système détecte les problèmes suivants : {e}")

        return redirect('liste_visiteur')
    
class Ajouter_sortieView(View):
    template_name = 'pages/forms/Ajouter_sortie.html'
    def get(self, request, *args, **kwargs):
        # Filtrez les enregistrements qui n'ont pas de sortie associée
        enregistrements = Enregistrement.objects.filter(sortie__isnull=True).order_by('-Date_heure_entree')
        context = {
            'enregistrements': enregistrements
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        enregistrement_id = request.POST.get('enregistrement')
        date_heure_sortie = request.POST.get('Date_heure_sortie')

        try:
            enregistrement = Enregistrement.objects.get(pk=enregistrement_id)
        except Enregistrement.DoesNotExist:
            # Gérez le cas où l'enregistrement n'existe pas
            pass

        if enregistrement:
            sortie = Sortie(
                enregistrement=enregistrement,
                Date_heure_sortie=date_heure_sortie
            )
            sortie.save()

        return redirect('liste_sortie') 
    
class ListeVisiteurView(View):
    template_name = 'pages/tables/liste_visiteur.html'
    items_per_page = 10

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search')
        enregistrements = Enregistrement.objects.all().order_by('-Date_heure_entree')

        if search_query:
            enregistrements = enregistrements.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(numero_telephone__icontains=search_query)
            )

        total_entries = enregistrements.count()

        paginator = Paginator(enregistrements, self.items_per_page)
        page = request.GET.get('page')
        enregistrements_page = paginator.get_page(page)

        context = {
            'enregistrements': enregistrements_page,
            'search_query': search_query,
            'total_entries': total_entries,
        }

        return render(request, self.template_name, context)
    
class ModifierEnregistrementView(View):
    template_name = 'pages/tables/modifier_enregistrement.html'

    def get(self, request, enregistrement_id, *args, **kwargs):
        enregistrement = get_object_or_404(Enregistrement, pk=enregistrement_id)

        # Vérifier si la modification est toujours autorisée
        if self.peut_modifier(enregistrement):
            form = EnregistrementcreateForm(instance=enregistrement)
            return render(request, self.template_name, {'enregistrement': enregistrement, 'form': form})
        else:
            # Retourner une réponse interdite si la modification n'est pas autorisée
            # Utilisation de SweetAlert pour afficher le message
            return HttpResponseForbidden("""
            <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
                             
                <script>
                document.addEventListener("DOMContentLoaded", function() {
    Swal.fire({
        title: "Modification non autorisée",
        text: "La modification n'est plus autorisée.",
        icon: 'error',
        showCancelButton: false,
        confirmButtonText: 'OK'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/table/liste_visiteur'; // Rediriger vers la page d'accueil
        }
    });
});
                </script>
            """)

    def post(self, request, enregistrement_id, *args, **kwargs):
        enregistrement = get_object_or_404(Enregistrement, pk=enregistrement_id)
        form = EnregistrementcreateForm(request.POST, instance=enregistrement)
        
        if form.is_valid():
            form.save()
            return redirect('liste_visiteur')  # Rediriger vers la page d'accueil après la modification

        return render(request, self.template_name, {'enregistrement': enregistrement, 'form': form})

    def peut_modifier(self, enregistrement):
        """
        Vérifie si la modification de l'enregistrement est autorisée en fonction du temps écoulé.
        """
        maintenant = timezone.now()
        deux_heures_plus_tard = enregistrement.Date_heure_entree + timedelta(hours=2)
        return maintenant <= deux_heures_plus_tard
class ExitpageView(View):
    template_name = 'pages/tables/liste_sortie.html'

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search')

        # Visiteurs sans sortie
        visiteurs_sans_sortie = Enregistrement.objects.exclude(sortie__isnull=False)

        # Sorties existantes
        sorties = Sortie.objects.all().order_by('-Date_heure_sortie').select_related('enregistrement')

        if search_query:
            # Filtrez les visiteurs sans sortie par recherche
            visiteurs_sans_sortie = visiteurs_sans_sortie.filter(
                Q(nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(numero_telephone__icontains=search_query)
            )

            # Filtrez les sorties par recherche
            sorties = sorties.filter(
                Q(enregistrement__nom__icontains=search_query) |
                Q(enregistrement__prenom__icontains=search_query) |
                Q(enregistrement__numero_telephone__icontains=search_query)
            )

        context = {
            'visiteurs_sans_sortie': visiteurs_sans_sortie,
            'sorties': sorties,
            'search_query': search_query,
        }

        return render(request, self.template_name, context)