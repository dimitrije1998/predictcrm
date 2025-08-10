import os
from dotenv import load_dotenv
from django.core.asgi import get_asgi_application

load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClientsList.settings')

api_key = os.getenv("OPENAI_API_KEY")

application = get_asgi_application()
