from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.trace import set_tracer_provider
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.django import DjangoInstrumentor
from django.conf import settings


def setup_tracing():
    """Set up Jaeger tracing with OpenTelemetry."""

    # Step 1: Initialize and set the concrete TracerProvider
    tracer_provider = TracerProvider()

    # Step 2: Create a resource for the service (i.e., your application)
    resource = Resource(
        attributes={
            "service.name": settings.SERVICE_NAME,
            "service.version": "1.0.0",
        }
    )

    # Step 3: Merge the resource with the TracerProvider's current resource (if any)
    new_resource = tracer_provider.resource.merge(resource)

    # Step 4: Assign the new resource to the TracerProvider
    tracer_provider = TracerProvider(resource=new_resource)

    # Step 5: Set the global TracerProvider
    set_tracer_provider(tracer_provider)

    # Step 6: Add a span processor to export spans to Jaeger
    tracer_provider.add_span_processor(
        BatchSpanProcessor(JaegerExporter(agent_host_name="localhost", agent_port=6831))
    )

    # Step 7: Instrument Django (or any other package you want to instrument)
    DjangoInstrumentor().instrument()
