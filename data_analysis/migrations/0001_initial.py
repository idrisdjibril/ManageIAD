# Generated by Django 5.1.1 on 2024-09-22 01:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_de_saisie', models.DateField()),
                ('valeur1', models.FloatField(blank=True, null=True)),
                ('valeur2', models.FloatField(blank=True, null=True)),
                ('valeur3', models.FloatField(blank=True, null=True)),
                ('categorie', models.CharField(blank=True, max_length=100, null=True)),
                ('commentaire', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Entrée de données',
                'verbose_name_plural': 'Entrées de données',
            },
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField()),
                ('result', models.JSONField(blank=True, null=True)),
                ('analysis_type', models.CharField(choices=[('table', 'Tableau statistique'), ('chart', 'Diagramme statistique')], max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Decision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('decision', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(choices=[('swot', 'Analyse SWOT'), ('cost_benefit', 'Analyse coûts-bénéfices'), ('risk_assessment', 'Évaluation des risques')], max_length=100)),
                ('justification', models.TextField()),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='data_analysis.analysis')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]