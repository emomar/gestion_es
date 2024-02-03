# Generated by Django 5.0.1 on 2024-01-12 16:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enregistrement',
            fields=[
                ('EnregistrementId', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('numero_telephone', models.CharField(max_length=15)),
                ('Date_heure_entree', models.DateTimeField(default=django.utils.timezone.now)),
                ('lieu_visite', models.CharField(max_length=100)),
                ('numero_badge', models.CharField(max_length=20)),
                ('reference_piece', models.CharField(max_length=50)),
                ('motif_visite', models.TextField()),
                ('societe', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photos/')),
                ('type_piece_identite', models.CharField(choices=[('CIN', "Pièce d'identité"), ('PC', 'Permis de conduire'), ('PP', 'Passeport'), ('CB', 'Carte biometrique'), ('NINA', 'Carte nina'), ('AU', 'Autre')], default='CIN', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='TypePieceIdentite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Sortie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date_heure_sortie', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('enregistrement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Emomar.enregistrement')),
            ],
        ),
    ]