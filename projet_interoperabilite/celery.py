# interoperabilite/celery.py

import os
from celery import Celery
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from collaboration import routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interoperabilite.settings')

app = Celery('interoperabilite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})