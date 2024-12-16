from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class OpenTelemetryAPIMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        with tracer.start_as_current_span("API Request") as span:
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.path", request.path)
            response = self.get_response(request)
            span.set_attribute("http.status_code", response.status_code)
            return response
