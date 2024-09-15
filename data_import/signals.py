#data_import/signals.py

from datetime import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ImportedData, Datasource
from django.core.mail import send_mail
from django.conf import settings
import os

@receiver(post_save, sender=ImportedData)
def imported_data_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Nouvelles données importées : {instance}")
        #Mettre à jour des statistiques
        update_import_statistics(instance)
        #Envoyer une notification
        send_import_notification(instance)
    else:
        print(f"Données importées mises à jour : {instance}")
        #Gérer la mise à jour des données existantes
        handle_data_update(instance)

@receiver(post_delete, sender=ImportedData)
def imported_data_post_delete(sender, instance, **kwargs):
    print(f"Données importées supprimées : {instance}")
    #Mettre à jour des compteurs
    update_import_counters(instance, deleted=True)
    #Nettoyer des fichiers associés
    clean_associated_files(instance)

@receiver(post_save, sender=Datasource)
def data_source_post_save(sender, instance, created, **kwargs):
    if created:
        print(f"Nouvelle source de données créée : {instance}")
        #Initialiser la nouvelle source de données
        initialize_data_source(instance)
    else:
        print(f"Source de données mise à jour : {instance}")
        #Gérer les mises à jour de la source de données
        handle_data_source_update(instance)

def update_import_statistics(instance):
    instance.data_source.total_records += instance.record_count
    instance.data_source.save()

def send_import_notification(instance):
    subject = f"Nouvelle importation de données pour {instance.data_source.name}"
    message = f"Une nouvelle importation de {instance.records_count} enregistrements a été effectuée."
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [settings.ADMIN_EMAIL])

def handle_data_update(instance):
    instance.last_updated = timezone.now()
    instance.update_count += 1
    instance.save()

def update_import_counters(instance, deleted=False):
    #Mettre à jour les compteurs liés aux importations
    if deleted:
        instance.data_source.total_records -= instance.record_count
        instance.data_source.save()

def clean_associated_files(instance):
    #Nettoyer les fichiers associés à l'importation supprimée
    if instance.file_path and os.path.exists(instance.file_path):
        os.remove(instance.file_path)

def initialize_data_source(instance):
    #initialiser la nouvelle source de données
    os.makedirs(os.path.join(settings.MEDIA_ROOT, f"imports/{instance.name}"), exist_ok=True)

def handle_data_source_update(instance):
    #Gérer les mises à jour de la source de données
    new_folder_path = os.path.join(settings.MEDIA_ROOT, f"imports/{instance.name}")
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path, exist_ok=True)

#Autres signaux potentiels

@receiver(post_save, sender=ImportedData)
def validate_imported_date(sender, instance, created, **kwargs):
    if created:
        #lancer un processus de validation des données importées
        from.tasks import validate_data
        validate_data.delay(instance.id)

@receiver(post_save, sender=Datasource)
def check_data_source_connection(sender, instance, created, **kwargs):
    #Vérifier la connexion à la source de données après création ou mise à jour
    from .utils import test_data_source_connextion
    test_data_source_connextion(instance)