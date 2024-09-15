from datetime import timezone
import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message, Folder, Group, Event, Task
from .forms import MessageForm, FolderForm, GroupForm, EventForm, TaskForm

@login_required
def collaboration(request):
    recent_messages = Message.objects.filter(recipient=request.user).order_by('-date')[:5]
    current_tasks = Task.objects.filter(assignee=request.user, completed=False).order_by('due_date')[:5]
    upcoming_events = Event.objects.filter(participants=request.user, start_time__gte=timezone.now()).order_by('start_time')[:5]
    return render(request, 'collaboration.html', {
        'recent_messages': recent_messages,
        'current_tasks': current_tasks,
        'upcoming_events': upcoming_events
    })

@login_required
def inbox(request):
    messages = Message.objects.filter(recipient=request.user).order_by('-date')
    return render(request, 'inbox.html', {'messages': messages})

@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('sent')
    else:
        form = MessageForm()
    return render(request, 'compose.html', {'form': form})

@login_required
def message_detail(request, message_id):
    message = Message.objects.get(id=message_id)
    if message.recipient == request.user and not message.read:
        message.read = True
        message.save()
    return render(request, 'message_detail.html', {'message': message})

@login_required
def sent(request):
    sent_messages = Message.objects.filter(sender=request.user).order_by('-date')
    return render(request, 'sent.html', {'sent_messages': sent_messages})

@login_required
def search_results(request):
    query = request.GET.get('q')
    results = Message.objects.filter(content__icontains=query) | Message.objects.filter(subject__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required
def folders(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.user = request.user
            folder.save()
            return redirect('folders')
    else:
        form = FolderForm()
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'folders.html', {'folders': folders, 'form': form})

@login_required
def groups(request):
    groups = Group.objects.filter(members=request.user)
    return render(request, 'groups.html', {'groups': groups})

@login_required
def calendar(request):
    return render(request, 'calendar.html')

@login_required
def get_events(request):
    events = Event.objects.filter(participants=request.user)
    event_list = [{'id': event.id, 'title': event.title, 'start': event.start_time, 'end': event.end_time} for event in events]
    return JsonResponse(event_list, safe=False)

@login_required
def tasks(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assignee = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    tasks = Task.objects.filter(assignee=request.user).order_by('due_date')
    return render(request, 'tasks.html', {'tasks': tasks, 'form': form})

@login_required
def update_task(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        task_id = data.get('taskId')
        completed = data.get('completed')
        task = Task.objects.get(id=task_id)
        task.completed = completed
        task.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)