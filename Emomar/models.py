
# Create your models here.
from django.db import models
from django.utils import timezone

class TypePieceIdentite(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Enregistrement(models.Model):
    PIECE_IDENTITE = 'CIN'
    PERMIS_CONDUIRE = 'PC'
    PASSEPORT = 'PP'
    CARTE_BIOMÉTRIQUE = 'CB'
    CARTE_NINA = 'NINA'
    AUTRE = 'AU'

    TYPE_PIECE_CHOICES = [
    ('CIN', "Pièce d'identité"),
    ('PC', "Permis de conduire"),
    ('PP', "Passeport"),
    ('CB', "Carte biometrique"),
    ('NINA', "Carte nina"),
    ('AU', "Autre"),
    ]


    EnregistrementId = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_telephone = models.CharField(max_length=15)
    Date_heure_entree = models.DateTimeField(default=timezone.now, null=False)
    lieu_visite = models.CharField(max_length=100)
    numero_badge = models.CharField(max_length=20)
    reference_piece = models.CharField(max_length=50)
    motif_visite = models.TextField()
    societe = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    # Nouveau champ ajouté
    type_piece_identite = models.CharField(
        max_length=7,
        choices=TYPE_PIECE_CHOICES,
        default=PIECE_IDENTITE,
    )

    def save(self, *args, **kwargs):
        # Générer le numéro de badge avec des zéros ajoutés au début
        # en fonction de la longueur spécifiée (ici, 3 pour ajouter 3 zéros)
        self.numero_badge = str(self.numero_badge).zfill(3)

        super(Enregistrement, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} {self.prenom} (ID: {self.EnregistrementId})"

class Sortie(models.Model):
    enregistrement = models.ForeignKey(Enregistrement, on_delete=models.CASCADE)
    Date_heure_sortie = models.DateTimeField(default=timezone.now, null=False, db_index=True)
    def get_photo_url(self):
        if self.enregistrement and self.enregistrement.photo:
            return self.enregistrement.photo.url
        return None

    def __str__(self):
        return f"Sortie de : {self.enregistrement.nom} {self.enregistrement.prenom} (Référence : {self.enregistrement.reference_piece}) à {self.Date_heure_sortie.strftime('%d %b %Y, %H:%M')} - Numéro de téléphone : {self.enregistrement.numero_telephone}, Numéro de badge : {self.enregistrement.numero_badge}"

# Récupérer tous les enregistrements
enregistrements = Enregistrement.objects.all()

# Créer une sortie pour chaque enregistrement
# Create your models here.
