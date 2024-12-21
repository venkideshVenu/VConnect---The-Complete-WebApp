from django.contrib.auth import get_user_model
from django.db import transaction

CustomUser = get_user_model()

# List of test users with their details
test_users = [
    {
        'username': 'sarah_wilson',
        'email': 'sarah.wilson@example.com',
        'password': 'SecurePass123!',
        'first_name': 'Sarah',
        'last_name': 'Wilson',
        'is_verified': True,
        'profile_completed': {'basic_info': True, 'preferences': True}
    },
    {
        'username': 'james_rodriguez',
        'email': 'james.r@example.com',
        'password': 'StrongPass456!',
        'first_name': 'James',
        'last_name': 'Rodriguez',
        'is_verified': True,
        'profile_completed': {'basic_info': True}
    },
    {
        'username': 'emily_chen',
        'email': 'emily.chen@example.com',
        'password': 'SafePass789!',
        'first_name': 'Emily',
        'last_name': 'Chen',
        'is_verified': True,
        'profile_completed': {'basic_info': True, 'preferences': True, 'avatar': True}
    },
    {
        'username': 'michael_brown',
        'email': 'michael.b@example.com',
        'password': 'ComplexPass321!',
        'first_name': 'Michael',
        'last_name': 'Brown',
        'is_verified': True,
        'profile_completed': {'basic_info': True, 'preferences': False}
    },
    {
        'username': 'lisa_patel',
        'email': 'lisa.patel@example.com',
        'password': 'UniquePass654!',
        'first_name': 'Lisa',
        'last_name': 'Patel',
        'is_verified': True,
        'profile_completed': {'basic_info': True, 'preferences': True}
    }
]

def create_test_users():
    """
    Create test users in the database
    """
    with transaction.atomic():
        for user_data in test_users:
            try:
                # Check if user already exists
                if not CustomUser.objects.filter(username=user_data['username']).exists():
                    user = CustomUser.objects.create_user(
                        username=user_data['username'],
                        email=user_data['email'],
                        password=user_data['password'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        is_verified=user_data['is_verified']
                    )
                    user.profile_completed = user_data['profile_completed']
                    user.save()
                    print(f"Created user: {user.username}")
                else:
                    print(f"User {user_data['username']} already exists")
            except Exception as e:
                print(f"Error creating user {user_data['username']}: {str(e)}")

if __name__ == "__main__":
    create_test_users()