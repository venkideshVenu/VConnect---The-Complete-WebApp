from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
import base64
from PIL import Image
import io

def create_test_data():
    # Get the CustomUser model
    CustomUser = get_user_model()
    
    # Create test instructor
    instructor = CustomUser.objects.create_user(
        username='test_instructor',
        email='instructor@example.com',
        password='test12345'
    )

    # Create Categories
    programming = Category.objects.create(title='Programming')
    design = Category.objects.create(title='Design')
    business = Category.objects.create(title='Business')
    data_science = Category.objects.create(title='Data Science')

    # Create a simple test image for thumbnails
    def create_test_image():
        # Create a simple colored image
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), 'blue')
        image.save(file, 'PNG')
        file.seek(0)
        return ContentFile(file.read(), name='test_thumbnail.png')

    # Create Courses
    courses_data = [
        {
            'title': 'Python Programming Masterclass',
            'user': instructor,
            'category': programming,
            'short_description': 'Comprehensive Python course from basics to advanced concepts',
            'description': '''This course covers everything you need to know about Python programming.
            From basic syntax to advanced topics like decorators, generators, and object-oriented programming.
            You'll learn through practical projects and real-world examples.''',
            'outcome': 'Build complex Python applications, Understand OOP, Work with APIs',
            'requirements': 'Basic computer skills, No prior programming experience needed',
            'language': 'English',
            'price': 49.99,
            'level': 'Beginner',
            'video_url': 'https://youtu.be/xyz123',
        },
        {
            'title': 'UI/UX Design Fundamentals',
            'user': instructor,
            'category': design,
            'short_description': 'Master modern UI/UX design principles and tools',
            'description': '''Learn the fundamentals of UI/UX design, including user research,
            wireframing, prototyping, and user testing. Master industry-standard tools like Figma.''',
            'outcome': 'Create user-centered designs, Build interactive prototypes, Conduct user research',
            'requirements': 'No prior design experience needed, Basic computer skills',
            'language': 'English',
            'price': 59.99,
            'level': 'Intermediate',
            'video_url': 'https://youtu.be/abc456',
        },
        {
            'title': 'Data Science with Python',
            'user': instructor,
            'category': data_science,
            'short_description': 'Learn data analysis and machine learning with Python',
            'description': '''Master data science using Python. Cover pandas, numpy, scikit-learn,
            and matplotlib. Build real-world machine learning projects and analyze complex datasets.''',
            'outcome': 'Analyze data with Python, Build ML models, Create data visualizations',
            'requirements': 'Basic Python knowledge, Understanding of statistics',
            'language': 'English',
            'price': 69.99,
            'level': 'Advanced',
            'video_url': 'https://youtu.be/def789',
        }
    ]

    created_courses = []
    for course_data in courses_data:
        course = Course.objects.create(
            title=course_data['title'],
            user=course_data['user'],
            category=course_data['category'],
            short_description=course_data['short_description'],
            description=course_data['description'],
            outcome=course_data['outcome'],
            requirements=course_data['requirements'],
            language=course_data['language'],
            price=course_data['price'],
            level=course_data['level'],
            video_url=course_data['video_url'],
            thumbnail=create_test_image()
        )
        created_courses.append(course)

    # Create Lessons
    lessons_data = [
        # Python Programming Masterclass lessons
        {
            'course': created_courses[0],
            'lessons': [
                {
                    'title': 'Introduction to Python',
                    'duration': 15.30,
                    'video_url': 'https://youtu.be/lesson1'
                },
                {
                    'title': 'Variables and Data Types',
                    'duration': 20.45,
                    'video_url': 'https://youtu.be/lesson2'
                },
                {
                    'title': 'Control Flow and Functions',
                    'duration': 25.15,
                    'video_url': 'https://youtu.be/lesson3'
                }
            ]
        },
        # UI/UX Design Fundamentals lessons
        {
            'course': created_courses[1],
            'lessons': [
                {
                    'title': 'Design Principles',
                    'duration': 18.20,
                    'video_url': 'https://youtu.be/lesson4'
                },
                {
                    'title': 'User Research Methods',
                    'duration': 22.30,
                    'video_url': 'https://youtu.be/lesson5'
                },
                {
                    'title': 'Prototyping in Figma',
                    'duration': 28.00,
                    'video_url': 'https://youtu.be/lesson6'
                }
            ]
        },
        # Data Science with Python lessons
        {
            'course': created_courses[2],
            'lessons': [
                {
                    'title': 'Data Analysis with Pandas',
                    'duration': 24.00,
                    'video_url': 'https://youtu.be/lesson7'
                },
                {
                    'title': 'Data Visualization',
                    'duration': 26.30,
                    'video_url': 'https://youtu.be/lesson8'
                },
                {
                    'title': 'Introduction to Machine Learning',
                    'duration': 29.45,
                    'video_url': 'https://youtu.be/lesson9'
                }
            ]
        }
    ]

    # Create all lessons
    for course_lessons in lessons_data:
        for lesson in course_lessons['lessons']:
            Lesson.objects.create(
                course=course_lessons['course'],
                title=lesson['title'],
                duration=lesson['duration'],
                video_url=lesson['video_url']
            )

    print("Test data created successfully!")
    return instructor, created_courses

# You can run this in Django shell:
# from your_app.utils import create_test_data
# instructor, courses = create_test_data()