from django.db import models
from django.conf import settings

class Analysis(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data = models.JSONField()
    result = models.JSONField(null=True, blank=True)
    analysis_type = models.CharField(max_length=10, choices=[('table', 'Tableau statistique'), ('chart', 'Diagramme statistique')])

class Decision(models.Model):
    DECISION_METHODS = [
        ('swot', 'Analyse SWOT'),
        ('cost_benefit', 'Analyse coûts-bénéfices'),
        ('risk_assessment', 'Évaluation des risques'),
    ]

    analysis = models.ForeignKey(Analysis, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    decision = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100, choices=DECISION_METHODS)
    justification = models.TextField()

class DataEntry(models.Model):
    date_de_saisie = models.DateField()
    valeur1 = models.FloatField(null=True, blank=True)
    valeur2 = models.FloatField(null=True, blank=True)
    valeur3 = models.FloatField(null=True, blank=True)
    categorie = models.CharField(max_length=100, null=True, blank=True)
    commentaire = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Entrée du {self.date_de_saisie}"

    class Meta:
        verbose_name = "Entrée de données"
        verbose_name_plural = "Entrées de données"