import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import plotly
from .models import Dataset, Analysis, SWOTAnalysis, CostBenefitAnalysis, MCDAAnalysis
from .forms import DatasetForm, AnalysisForm, SWOTAnalysisForm, CostBenefitAnalysisForm, MCDAAnalysisForm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.db.models import Q
import plotly.graph_objs as go
import plotly.io as pio

# ... (les fonctions existantes restent inchangées)

@login_required
def create_swot_analysis(request):
    if request.method == 'POST':
        form = SWOTAnalysisForm(request.POST)
        if form.is_valid():
            swot = form.save(commit=False)
            swot.user = request.user
            swot.save()
            return redirect('swot_analysis_detail', pk=swot.pk)
    else:
        form = SWOTAnalysisForm()
    return render(request, 'data_analysis/create_swot_analysis.html', {'form': form})

@login_required
def swot_analysis_detail(request, pk):
    swot = get_object_or_404(SWOTAnalysis, pk=pk, user=request.user)
    return render(request, 'data_analysis/swot_analysis_detail.html', {'swot': swot})

@login_required
def create_cost_benefit_analysis(request):
    if request.method == 'POST':
        form = CostBenefitAnalysisForm(request.POST)
        if form.is_valid():
            cba = form.save(commit=False)
            cba.user = request.user
            cba.save()
            return redirect('cost_benefit_analysis_detail', pk=cba.pk)
    else:
        form = CostBenefitAnalysisForm()
    return render(request, 'data_analysis/create_cost_benefit_analysis.html', {'form': form})

@login_required
def cost_benefit_analysis_detail(request, pk):
    cba = get_object_or_404(CostBenefitAnalysis, pk=pk, user=request.user)
    
    costs = cba.costs
    benefits = cba.benefits
    
    total_costs = sum(costs.values())
    total_benefits = sum(benefits.values())
    net_benefit = total_benefits - total_costs
    benefit_cost_ratio = total_benefits / total_costs if total_costs != 0 else float('inf')
    
    # Créer un graphique pour les coûts et les bénéfices
    fig = go.Figure(data=[
        go.Bar(name='Coûts', x=list(costs.keys()), y=list(costs.values())),
        go.Bar(name='Bénéfices', x=list(benefits.keys()), y=list(benefits.values()))
    ])
    fig.update_layout(barmode='group', title='Analyse Coûts-Bénéfices')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    context = {
        'cba': cba,
        'total_costs': total_costs,
        'total_benefits': total_benefits,
        'net_benefit': net_benefit,
        'benefit_cost_ratio': benefit_cost_ratio,
        'graph_json': graph_json
    }
    return render(request, 'data_analysis/cost_benefit_analysis_detail.html', context)

@login_required
def create_mcda_analysis(request):
    if request.method == 'POST':
        form = MCDAAnalysisForm(request.POST)
        if form.is_valid():
            mcda = form.save(commit=False)
            mcda.user = request.user
            mcda.save()
            return redirect('mcda_analysis_detail', pk=mcda.pk)
    else:
        form = MCDAAnalysisForm()
    return render(request, 'data_analysis/create_mcda_analysis.html', {'form': form})

@login_required
def mcda_analysis_detail(request, pk):
    mcda = get_object_or_404(MCDAAnalysis, pk=pk, user=request.user)
    
    # Calculer les scores pondérés
    weighted_scores = {}
    for alternative in mcda.alternatives:
        weighted_scores[alternative] = sum(mcda.scores[alternative][criterion] * mcda.weights[criterion] for criterion in mcda.criteria)
    
    # Trouver la meilleure alternative
    best_alternative = max(weighted_scores, key=weighted_scores.get)
    
    # Créer un graphique pour les scores pondérés
    fig = go.Figure(data=[go.Bar(x=list(weighted_scores.keys()), y=list(weighted_scores.values()))])
    fig.update_layout(title='Scores pondérés des alternatives', xaxis_title='Alternatives', yaxis_title='Score pondéré')
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    context = {
        'mcda': mcda,
        'weighted_scores': weighted_scores,
        'best_alternative': best_alternative,
        'graph_json': graph_json
    }
    return render(request, 'data_analysis/mcda_analysis_detail.html', context)