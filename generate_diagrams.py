import os
import django
from django.apps import apps

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VConnect.settings')  # Replace with your project name
django.setup()

# Define the base directory for storing diagrams
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIAGRAMS_DIR = os.path.join(BASE_DIR, "diagrams")

# Create diagrams directory if it doesn't exist
if not os.path.exists(DIAGRAMS_DIR):
    os.makedirs(DIAGRAMS_DIR)

# Generate diagrams for each app and convert to images
for app in apps.get_app_configs():
    app_name = app.name
    app_diagram_dir = os.path.join(DIAGRAMS_DIR, app_name)

    if not os.path.exists(app_diagram_dir):
        os.makedirs(app_diagram_dir)

    # Generate the .dot file
    dot_file = os.path.join(app_diagram_dir, "models.dot")
    os.system(f"python manage.py graph_models {app_name} --output {dot_file}")

    # Convert the .dot file to an image
    if os.path.exists(dot_file):  # Ensure the .dot file was created
        image_file = dot_file.replace(".dot", ".png")
        os.system(f"dot -Tpng {dot_file} -o {image_file}")
        print(f"Generated image: {image_file}")
    else:
        print(f"Failed to generate .dot file for app: {app_name}")
