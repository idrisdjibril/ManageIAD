from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db.models import Q
from .models import Analysis, Decision, DataEntry
from .forms import AnalysisForm, DecisionForm
from data_import.models import DHIS2Data
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import PyPDF2

@login_required
def select_data(request):
    if request.method == 'POST':
        column_count = int(request.POST.get('column_count', 0))
        columns = request.POST.getlist('columns')
        date_selection = request.POST.get('date_selection')
        
        if 'pdf_file' in request.FILES:
            # Handle PDF file upload
            pdf_file = request.FILES['pdf_file']
            # Process the PDF file and extract data
            # This is a placeholder, you'll need to implement PDF parsing logic
            selected_data = [{'data': 'from PDF'}]
        else:
            # Fetch data from DHIS2Data model
            selected_data = DHIS2Data.objects.filter(_date_de_saisie__startswith=date_selection).values(*columns)
        
        request.session['selected_data'] = list(selected_data)
        request.session['selected_columns'] = columns
        return redirect('analysis')
    
    data_columns = [f.name for f in DHIS2Data._meta.get_fields()]
    return render(request, 'data_analysis/select_data.html', {'data_columns': data_columns})

@login_required
def analysis(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.data = request.session.get('selected_data', [])
            analysis.save()
            
            analysis_type = request.POST.get('analysis_type')
            if analysis_type == 'table':
                return redirect('statistical_table', analysis_id=analysis.id)
            else:
                return redirect('visualization', analysis_id=analysis.id)
    else:
        form = AnalysisForm()
    
    analyses = Analysis.objects.filter(user=request.user)
    selected_data = request.session.get('selected_data', None)
    selected_columns = request.session.get('selected_columns', None)
    return render(request, 'data_analysis/analysis.html', {
        'form': form, 
        'analyses': analyses,
        'selected_data': selected_data,
        'selected_columns': selected_columns,
    })

@login_required
def visualization(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)
    df = pd.DataFrame(analysis.data)
    
    if request.method == 'POST':
        chart_type = request.POST.get('chart_type')
        x_axis = request.POST.get('x_axis')
        y_axis = request.POST.get('y_axis')
        
        plt.figure(figsize=(10, 6))
        if chart_type == 'bar':
            df.plot(kind='bar', x=x_axis, y=y_axis)
        elif chart_type == 'line':
            df.plot(kind='line', x=x_axis, y=y_axis)
        elif chart_type == 'scatter':
            df.plot(kind='scatter', x=x_axis, y=y_axis)
        elif chart_type == 'pie':
            df[y_axis].plot(kind='pie', labels=df[x_axis], autopct='%1.1f%%')
        elif chart_type == 'histogram':
            df[y_axis].hist(bins=10)
            plt.xlabel(y_axis)
        
        plt.title(f'{chart_type.capitalize()} : {x_axis} vs {y_axis}')
        plt.xlabel(x_axis);
        plt.ylabel(y_axis);
        
        buffer = io.BytesIO();
        plt.savefig(buffer, format='png');
        buffer.seek(0);
        image_png = buffer.getvalue();
        buffer.close();
        
        graphic = base64.b64encode(image_png);
        graphic = graphic.decode('utf-8');
        
        return JsonResponse({'graphic': graphic});
    
    return render(request, 'data_analysis/visualization.html', {'analysis': analysis});

@user_passes_test(lambda u: u.role == 'directeur')
def decision_making(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id);
    
    if request.method == 'POST':
        form = DecisionForm(request.POST);
        if form.is_valid():
            decision = form.save(commit=False);
            decision.analysis = analysis;
            decision.user = request.user;
            decision.save();
            return redirect('analysis');
    else:
        form = DecisionForm();
    
    return render(request, 'data_analysis/decision_making.html', {'form': form, 'analysis': analysis});

@login_required
def statistical_table(request, analysis_id):
    analysis = get_object_or_404(Analysis, id=analysis_id)
    df = pd.DataFrame(analysis.data)
    
    # Tableau de fréquences
    freq_table = df.apply(pd.Series.value_counts).fillna(0)
    freq_html = freq_table.to_html(classes='table table-striped')
    
    # Statistiques descriptives
    desc_stats = df.describe().to_html(classes='table table-striped')
    
    # Tableau croisé (exemple avec les deux premières colonnes)
    if len(df.columns) >= 2:
        cross_tab = pd.crosstab(df[df.columns[0]], df[df.columns[1]])
        cross_html = cross_tab.to_html(classes='table table-striped')
    else:
        cross_html = "Pas assez de colonnes pour un tableau croisé"
    
    # Matrice de corrélation
    corr_matrix = df.corr()
    corr_html = corr_matrix.to_html(classes='table table-striped')
    
    context = {
        'analysis': analysis,
        'freq_table': freq_html,
        'desc_stats': desc_stats,
        'cross_tab': cross_html,
        'corr_matrix': corr_html
    }
    
    return render(request, 'data_analysis/statistical_table.html', context)

login_required
def create_analysis(request):
    if request.method == 'POST':
        form = AnalysisForm(request.POST, request.FILES)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.save()
            
            # Traitement des données
            data = process_uploaded_data(request.FILES['data_file'])
            analysis.data = data
            analysis.save()
            
            return redirect('analysis_detail', analysis_id=analysis.id)
    else:
        form = AnalysisForm()
    
    return render(request, 'data_analysis/create_analysis.html', {'form': form})

def process_uploaded_data(file):
    # Logique pour traiter le fichier uploadé
    # Par exemple, lire un fichier CSV avec pandas
    import pandas as pd
    df = pd.read_csv(file)
    return df.to_dict('records')  # Convertir DataFrame en liste de dictionnaires

@csrf_exempt
@require_POST
def get_selected_data(request):
    data = json.loads(request.body)
    columns = data.get('columns', [])
    date = data.get('date', '')
    
    if '_date_de_saisie_' not in columns:
        columns.append('_date_de_saisie_')
    
    try:
        # Utilisez Q pour filtrer la date en ignorant la partie heure
        selected_data = DataEntry.objects.filter(
            Q(_date_de_saisie__startswith=date)
        ).values(*columns)
        rows = list(selected_data)
    except Exception as e:
        # En cas d'erreur, on revient aux données factices
        rows = [{'_date_de_saisie_': f"{date} 00:00:00.0", **{col: f'Data for {col}' for col in columns}}]
    
    response_data = {
        'columns': columns,
        'rows': rows
    }
    
    return JsonResponse(response_data, encoder=DjangoJSONEncoder)