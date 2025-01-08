from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.django import DjangoInstrumentor


def setup_jaeger_tracing():
    """Set up Jaeger exporter for OpenTelemetry."""
    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",  # Jaeger agent host
        agent_port=6831,  # Jaeger agent port
    )

    # Set up BatchSpanProcessor to send spans to Jaeger
    span_processor = BatchSpanProcessor(jaeger_exporter)

    # Set the TracerProvider and add the span processor
    tracer_provider = TracerProvider()
    tracer_provider.add_span_processor(span_processor)

    # Step 5: Instrument Django (or any other package you want to instrument)
    DjangoInstrumentor().instrument()

    # # Set the TracerProvider as the global tracer provider
    # get_tracer_provider().add_span_processor(span_processor)
