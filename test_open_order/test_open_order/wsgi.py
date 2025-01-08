"""
WSGI config for test_open project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

from opentelemetry.instrumentation.django import DjangoInstrumentor
from .otel_setting import setup_tracing
from .jeager_tracing import setup_jaeger_tracing

# Initialize Jaeger tracing
setup_jaeger_tracing()
setup_tracing("TestOpenOrder")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_open_order.settings")

# Instrument Django with OpenTelemetry
DjangoInstrumentor().instrument()
application = get_wsgi_application()
