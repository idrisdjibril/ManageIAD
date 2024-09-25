from django import forms
from .models import Analysis, Decision

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['title', 'description', 'analysis_type']

class DecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = ['decision', 'method', 'justification']
        widgets = {
            'method': forms.Select(choices=Decision.DECISION_METHODS),
        }