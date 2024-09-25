from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard_admin.html')

@login_required
def dashboard_director(request):
    return render(request, 'dashboard_director.html')

@login_required
def dashboard_agent(request):
    return render(request, 'dashboard_agent.html')

@login_required
def data_table(request):
    return render(request, 'data_table.html')

@login_required
def visualization(request):
    return render(request, 'visualization.html')

@login_required
def decision_making(request):
    return render(request, 'decision_making.html')

@login_required
def user_list(request):
    return render(request, 'user_list.html')

@login_required
def compose(request):
    return render(request, 'compose.html')

@login_required
def edit_profile(request):
    return render(request, 'edit_profile.html')