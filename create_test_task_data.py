# test_data.py

from django.utils import timezone
from datetime import timedelta
from tasks.models import Project, Task, TaskComment
from django.contrib.auth import get_user_model

User = get_user_model()

# Create test users
user1 = User.objects.create_user(username='john_doe', email='john@example.com', password='password123')
user2 = User.objects.create_user(username='jane_smith', email='jane@example.com', password='password123')

# Create projects
project1 = Project.objects.create(
    name='Website Redesign',
    description='Complete overhaul of company website',
    owner=user1
)

project2 = Project.objects.create(
    name='Mobile App Development',
    description='Develop iOS and Android applications',
    owner=user1
)

# Create tasks
tasks = [
    Task.objects.create(
        title='Design Homepage',
        description='Create new homepage mockup',
        project=project1,
        assigned_to=user1,
        created_by=user1,
        due_date=timezone.now() + timedelta(days=7),
        priority='high',
        status='in_progress'
    ),
    Task.objects.create(
        title='Setup Database',
        description='Configure and optimize database',
        project=project1,
        assigned_to=user2,
        created_by=user1,
        due_date=timezone.now() + timedelta(days=3),
        priority='medium',
        status='todo'
    ),
    Task.objects.create(
        title='iOS Development',
        description='Develop iOS version of the app',
        project=project2,
        assigned_to=user2,
        created_by=user1,
        due_date=timezone.now() + timedelta(days=14),
        priority='high',
        status='todo'
    )
]

# Create comments
TaskComment.objects.create(
    task=tasks[0],
    user=user1,
    content='Homepage mockup first draft completed'
)

TaskComment.objects.create(
    task=tasks[0],
    user=user2,
    content='Need to adjust color scheme'
)

print("Test data created successfully!")