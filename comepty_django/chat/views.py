from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Conversation, Message


@login_required
def inbox(request):
    conversations_raw = request.user.conversations.prefetch_related('participants', 'messages').order_by('-updated_at')
    conversations = []
    for conv in conversations_raw:
        other = conv.participants.exclude(id=request.user.id).first()
        last_msg = conv.messages.order_by('-created_at').first()
        conversations.append({'conv': conv, 'other': other, 'last_msg': last_msg})
    return render(request, 'chat/inbox.html', {'conversations': conversations})


@login_required
def start_conversation(request, username):
    other_user = get_object_or_404(User, username=username)
    if other_user == request.user:
        return redirect('inbox')
    existing = Conversation.objects.filter(participants=request.user).filter(participants=other_user)
    if existing.exists():
        conv = existing.first()
    else:
        conv = Conversation.objects.create()
        conv.participants.add(request.user, other_user)
    return redirect('conversation_detail', pk=conv.pk)


@login_required
def conversation_detail(request, pk):
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    other_user = conv.participants.exclude(id=request.user.id).first()

    conv.messages.exclude(sender=request.user).update(is_read=True)

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            msg = Message.objects.create(conversation=conv, sender=request.user, text=text)
            conv.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': msg.id,
                    'text': msg.text,
                    'sender': msg.sender.username,
                    'created_at': msg.created_at.strftime('%H:%M'),
                    'is_mine': True,
                })

    messages_qs = conv.messages.select_related('sender').all()

    sidebar_convs = []
    for c in request.user.conversations.prefetch_related('participants', 'messages').order_by('-updated_at'):
        other = c.participants.exclude(id=request.user.id).first()
        last_msg = c.messages.order_by('-created_at').first()
        sidebar_convs.append({'conv': c, 'other': other, 'last_msg': last_msg})

    return render(request, 'chat/conversation.html', {
        'conversation': conv,
        'other_user': other_user,
        'chat_messages': messages_qs,  # Safely separated context key
        'sidebar_convs': sidebar_convs,
    })


@login_required
def poll_messages(request, pk):
    """Returns new messages after a given message ID — used for real-time polling."""
    conv = get_object_or_404(Conversation, pk=pk, participants=request.user)
    after_id = int(request.GET.get('after', 0))
    new_msgs = conv.messages.filter(id__gt=after_id).select_related('sender').order_by('created_at')
    new_msgs.exclude(sender=request.user).update(is_read=True)
    data = [
        {
            'id': m.id,
            'text': m.text,
            'sender': m.sender.username,
            'is_mine': m.sender_id == request.user.id,
            'created_at': m.created_at.strftime('%H:%M'),
        }
        for m in new_msgs
    ]
    return JsonResponse({'messages': data})


@login_required
def edit_message(request, msg_id):
    if request.method == 'POST':
        msg = get_object_or_404(Message, id=msg_id, sender=request.user)
        new_text = request.POST.get('text', '').strip()
        if new_text:
            msg.text = new_text
            msg.save()
            return JsonResponse({'status': 'success', 'text': msg.text})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def delete_message(request, msg_id):
    if request.method == 'POST':
        msg = get_object_or_404(Message, id=msg_id, sender=request.user)
        msg.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)