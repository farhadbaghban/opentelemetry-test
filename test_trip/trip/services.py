import requests
from django.conf import settings
from opentelemetry import trace
from opentelemetry.propagate import inject

from opentelemetry.trace import SpanKind

tracer = trace.get_tracer("django-app")
USER_SERVICE_URL = settings.USER_SERVICE_URL
ORDER_SERVICE_URL = settings.ORDER_SERVICE_URL


def make_request_with_tracing(url: str, request: requests):
    try:
        # Create a mutable copy of the headers
        headers = {key: value for key, value in request.headers.items()}
        headers["Accept"] = "application/json" 
        inject(headers)
        # Make the HTTP request with the trace context in headers
        response = requests.get(url, headers=headers)
        return response
    except Exception:
        return None


def get_user(request: requests):
    user_id = request.data.get("user_id")
    with tracer.start_as_current_span("get_user_from_service", kind=SpanKind.SERVER):
        url = f"{USER_SERVICE_URL}/{user_id}/"
        response = make_request_with_tracing(url=url, request=request)
        response.raise_for_status()
        return response.json()


def get_order(request: requests):
    order_id = request.data.get("order_id")
    with tracer.start_as_current_span("get_order_from_service", kind=SpanKind.SERVER):
        url = f"{ORDER_SERVICE_URL}/orders/{order_id}/"
        response = make_request_with_tracing(url=url, request=request)
        response.raise_for_status()
        return response.json()


def get_order_items(request: requests):
    order_id = request.data.get("order_id")
    with tracer.start_as_current_span(
        "get_order_item_from_service", kind=SpanKind.SERVER
    ):
        url = f"{ORDER_SERVICE_URL}/orders/{order_id}/items/"
        response = make_request_with_tracing(url=url, request=request)
        response.raise_for_status()
        return response.json()
