from django.shortcuts import render, redirect
from core.models import CustomUser  # Import your CustomUser model
from .models import ChatRoom, Message

def chat_list(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name')
        participants_usernames = request.POST.getlist('participants')

        chat_room = ChatRoom.objects.create(
            room_name="group_"+str(ChatRoom.objects.count() + 1),
            is_group_chat=True,
            group_name=group_name
        )

        chat_room.participants.add(request.user)

        participants = CustomUser.objects.filter(username__in=participants_usernames)  # Changed from User to CustomUser
        chat_room.participants.add(*participants)

        return redirect('chat:chat_list')

    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    # You'll need to adjust this based on how you handle followers in your CustomUser model
    all_participants = CustomUser.objects.exclude(id=request.user.id)  # Modified to show all users except current user

    context = {'chat_rooms': chat_rooms, 'all_participants': all_participants}
    return render(request, "chat/chat_list.html", context)

def chat(request, username: str):
    chat_user = CustomUser.objects.get(username=username)  # Changed from User to CustomUser
    room_name = f"room_{min(chat_user.id, request.user.id)}_{max(chat_user.id, request.user.id)}"
    
    chat_room, created = ChatRoom.objects.get_or_create(room_name=room_name)
    chat_room.participants.add(request.user)
    
    messages = Message.objects.filter(room=chat_room).order_by('timestamp')

    context = {
        "room_name": room_name,
        "chat_user": chat_user,
        "history_messages": messages
    }

    return render(request, "chat/chat.html", context)

def group_chat(request, room_name):
    try:
        chat_room = ChatRoom.objects.get(room_name=room_name, is_group_chat=True)
    except ChatRoom.DoesNotExist:
        return render(request, "chat/group_chat_not_found.html")

    participants = chat_room.participants.values_list('id', flat=True)
    messages = Message.objects.filter(room=chat_room).order_by('timestamp')

    context = {
        "room_name": room_name,
        "participants": participants,
        "history_messages": messages,
        "chat_room": chat_room
    }

    return render(request, "chat/group_chat.html", context)