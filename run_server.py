import os
import sys
import subprocess

def run_tests():
    print("Exécution des tests...")
    result = subprocess.run(['python', 'manage.py', 'test', 'data_analysis'], capture_output=True, text=True)
    if result.returncode != 0:
        print("Les tests ont échoué. Veuillez corriger les erreurs avant de démarrer le serveur.")
        print(result.stdout)
        print(result.stderr)
        return False
    print("Tous les tests ont réussi.")
    return True

def run_server():
    print("Démarrage du serveur de développement...")
    os.execvp('python', ['python', 'manage.py', 'runserver'])

if __name__ == "__main__":
    if run_tests():
        run_server()