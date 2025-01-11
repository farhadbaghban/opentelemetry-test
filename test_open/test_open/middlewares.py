from opentelemetry import trace
from django.db import connection
import time
from django.conf import settings
from opentelemetry.trace import get_current_span, SpanKind, Status
from opentelemetry.propagate import inject
from opentelemetry.propagate import extract
from opentelemetry.context import attach, detach

tracer = trace.get_tracer(__name__)


class TraceMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract tracing context from incoming headers
        carrier = {k.lower(): v for k, v in request.headers.items()}
        context = extract(carrier)
        token = attach(context)
        try:
            span = get_current_span()
            if span and span.get_span_context().is_valid:
                with span:
                    print(span.get_span_context())
                    response =  self.set_span_data(span,request)
            else:
                
                with tracer.start_as_current_span(
                    f"{request.method} {request.path} - {settings.SERVICE_NAME}",
                    kind=SpanKind.SERVER
                ) as span:
                    response = self.set_span_data(span,request)

        except Exception as e:
            if span:
                span.record_exception(e)
                span.set_status(Status(trace.StatusCode.ERROR, str(e)))
            raise
        finally:
            detach(token)

        return response
    
    def set_span_data(self,span,request):
        # Record the HTTP method and path
        span.set_attribute("http.method", request.method)
        span.set_attribute("http.path", request.path)

        # Start a timer to measure the total request time
        start_time = time.time()

        # Capture the initial state of database queries
        initial_query_count = len(connection.queries)

        # Process the request and capture the response
        response = self.get_response(request)

        # Calculate the total time taken for the request
        total_time = time.time() - start_time

        # Capture the final state of database queries
        total_queries = len(connection.queries) - initial_query_count
        query_time = sum(
            float(query["time"])
            for query in connection.queries[initial_query_count:]
        )

        # Record additional details into the span
        span.set_attribute("http.status_code", response.status_code)
        span.set_attribute("total_request_time", total_time)
        span.set_attribute("db.query_count", total_queries)
        span.set_attribute("db.query_time", query_time)

        # Optionally log individual queries for detailed insights
        for idx, query in enumerate(
            connection.queries[initial_query_count:], start=1
        ):
            span.add_event(
                f"Query {idx}",
                attributes={
                    "sql": query["sql"],
                    "time": query["time"],
                },
            )
        # Create a mutable copy of headers
        mutable_headers = {k: v for k, v in request.headers.items()}

        # Inject tracing context into the mutable headers
        inject(mutable_headers)    
        return response