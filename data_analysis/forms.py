from django import forms
from .models import Dataset, Analysis, SWOTAnalysis, CostBenefitAnalysis, MCDAAnalysis

class DatasetForm(forms.ModelForm):
    class Meta:
        model = Dataset
        fields = ['name', 'description', 'file']

class AnalysisForm(forms.ModelForm):
    class Meta:
        model = Analysis
        fields = ['name', 'description', 'chart_type', 'x_axis', 'y_axis']

class DateRangeForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class CategoryFilterForm(forms.Form):
    category = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = categories

class ValueRangeForm(forms.Form):
    value_min = forms.FloatField()
    value_max = forms.FloatField()

class SWOTAnalysisForm(forms.ModelForm):
    class Meta:
        model = SWOTAnalysis
        fields = ['name', 'strengths', 'weaknesses', 'opportunities', 'threats']

class CostBenefitAnalysisForm(forms.ModelForm):
    class Meta:
        model = CostBenefitAnalysis
        fields = ['name', 'costs', 'benefits']

class MCDAAnalysisForm(forms.ModelForm):
    class Meta:
        model = MCDAAnalysis
        fields = ['name', 'criteria', 'alternatives', 'weights', 'scores']