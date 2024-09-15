import psycopg2
import requests
import csv
import os
from django.conf import settings
from django.db import connections

def test_data_source_connection(data_source):
    #Fontion pour tester la connexion à une source de données en fonction de son type.
    print(f"Tentative de connexion à la source de données : {data_source.name} (Type: {data_source.type})")
    try:
        if data_source.type == 'PostgreSQL':
            return test_postgresql_connection(data_source)
        elif data_source.type == 'API':
            return test_api_connection(data_source)
        elif data_source.type == 'CSV':
            return test_csv_file_existence(data_source)
        elif data_source.type == 'Django':
            return test_django_db_connection(data_source)
        else:
            print(f"Type de source de données non pris en charge : {data_source.type}")
            return False
    except Exception as e:
        print(f"Erreur lors de la connexion à {data_source.name}: {str(e)}")
        return False

def test_postgresql_connection(data_source):
    #Teste la connexion à une base de données PostgreSQL
    try:
        conn = psycopg2.connect(
            dbname=data_source.database_nme,
            user=data_source.username,
            password=data_source.password,
            host=data_source.host,
            port=data_source.port
        )
        with conn.cursor() as cur:
            cur.execute("SLECT 1")
        conn.close()
        print(f"Connexion PostreSQL réussie pour {data_source.name}: {str(e)}")
        return True
    except psycopg2.Error as e:
        print(f"Echec de la connexion PostgreSQL pour {data_source.name}: {str(e)}")
        return False

def test_api_connection(data_source):
    #Teste une connexion à une API
    try:
        response = requests.get(data_source.url, headers=data_source.headers, timeout=10)
        if response.status_code == 200:
            print(f"Connexion API réussie pour {data_source.name}")
            return True
        else:
            print(f"Echec de la connexion API pour {data_source.name}. Status code: {response.status_code}")
            return False
    except requests.RequestException as e:
        print(f"Erreur de connexion API pour {data_source.name}: {str(e)}")
        return False

def test_csv_file_existence(data_source):
    #Vérifier l'existence et la validité d'un fichier CSV
    file_path = os.path.join(settings.MEDIA_ROOT, data_source.file_path)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                next(csv_reader) #véfifie si le fichier peut être lu et a au moins une ligne
                print(f"Fichier CSV valide trouvé pour {data_source.name}")
                return True
        except Exception as e:
            print(f"Fichier CSV trouvé mais invalide pour {data_source.name}: {str(e)}")
            return False
        else:
            print(f"Fichier CSV trouvé pour {data_source.name}")
            return False

def test_django_db_connection(data_source):
    #Teste la connexion à une base de données configurée dans Django
    try:
        connection = connections[data_source.django_db_alias]
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print(f"Connexion à la base de données Django réussie pour {data_source.name}")
            return True
    except Exception as e:
        print(f"Echec de la connexion à la base de données Django pour {data_source.name}: {str(e)}")
        return False