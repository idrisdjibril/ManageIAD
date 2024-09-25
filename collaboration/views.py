from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
import json
from django.db.models import Q
from .models import Message, Tag, Attachment
from .forms import MessageForm, TagForm
from django.contrib.auth import get_user_model
import psycopg2
from django.views.decorators.http import require_http_methods


def get_users_from_database():
    User = get_user_model()
    return [{'username': user.username} for user in User.objects.all()]

@login_required
def inbox(request, recipient_username=None):
    User = get_user_model()
    
    if recipient_username:
        recipient = get_object_or_404(User, username=recipient_username)
        messages = Message.objects.filter(
            ((Q(sender=request.user) & Q(recipient=recipient)) |
             (Q(sender=recipient) & Q(recipient=request.user))) &
            (Q(is_deleted_by_sender=False) | Q(is_deleted_by_recipient=False))
        ).order_by('created_at')
        
        if request.method == 'POST':
            form = MessageForm(request.POST, request.FILES, user=request.user)
            if form.is_valid():
                message = form.save(commit=False)
                message.sender = request.user
                message.recipient = recipient
                message.save()
                form.save_m2m()  # Save tags
                return redirect('inbox', recipient_username=recipient_username)
        else:
            form = MessageForm(user=request.user, initial={'recipient': recipient})
        
        context = {
            'messages': messages,
            'recipient': recipient,
            'form': form
        }
    else:
        conversations = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).values('sender', 'recipient').distinct()
        
        unique_users = set()
        for conv in conversations:
            unique_users.add(conv['sender'])
            unique_users.add(conv['recipient'])
        unique_users.discard(request.user.id)
        
        users = User.objects.filter(id__in=unique_users)
        context = {
            'users': users
        }
    
    return render(request, 'collaboration/inbox.html', context)

@login_required
def compose(request):
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            form.save_m2m()  # Save tags
            
            # Handle file attachment
            if 'attachment' in request.FILES:
                attachment = Attachment(file=request.FILES['attachment'], message=message)
                attachment.save()
            
            return redirect('inbox')
    else:
        form = MessageForm(user=request.user)
    
    users = get_users_from_database()
    return render(request, 'collaboration/compose.html', {'form': form, 'users': users})

@login_required
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.recipient == request.user and not message.read_at:
        message.read_at = timezone.now()
        message.save()
    return render(request, 'collaboration/message_detail.html', {'message': message})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user == message.sender:
        message.is_deleted_by_sender = True
    elif request.user == message.recipient:
        message.is_deleted_by_recipient = True
    message.save()
    return redirect('inbox')

@login_required
def mark_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, recipient=request.user)
    message.read_at = timezone.now()
    message.save()
    return JsonResponse({'status': 'success'})

@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return JsonResponse({'id': tag.id, 'name': tag.name})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@require_http_methods(["POST"])
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, sender=request.user)
    data = json.loads(request.body)
    message.subject = data.get('subject', message.subject)
    message.body = data.get('body', message.body)
    message.save()
    return JsonResponse({'status': 'success'})

def get_users_from_database():
    conn = psycopg2.connect(
        dbname="interoperabilite",
        user="landry",
        password="12345",
        host="localhost"
    )
    cur = conn.cursor()
    cur.execute("SELECT username FROM authentication_authenticate")
    users = [{'username': row[0]} for row in cur.fetchall()]
    cur.close()
    conn.close()
    return users

@login_required
def get_users(request):
    users = get_users_from_database()
    return JsonResponse(users, safe=False)