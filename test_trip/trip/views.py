from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Trip, Location
from .serializers import TripSerializer
from .services import get_user, get_order
from opentelemetry import trace
from .tasks import send_request

tracer = trace.get_tracer("django-app")


class TripView(APIView):
    def post(self, request):
        with tracer.start_as_current_span("trip_post_span"):
            data = request.data

            # Fetch user and order data from external services
            user = get_user(request)
            order = get_order(request)
            if user is None:
                return Response("user not found", status=status.HTTP_404_NOT_FOUND)
            if order is None:
                return Response("order not found", status=status.HTTP_404_NOT_FOUND)
            # Validate and create locations
            pickup_location_data = data["pickup_location"]
            dropoff_location_data = data["dropoff_location"]

            pickup_location = Location.objects.create(**pickup_location_data)
            dropoff_location = Location.objects.create(**dropoff_location_data)
            user_id = user.get("id")
            order_id = order.get("id")
            # Create trip
            trip = Trip.objects.create(
                user_id=user_id,
                order_id=order_id,
                pickup_location=pickup_location,
                dropoff_location=dropoff_location,
                status="pending",
            )
            response = TripSerializer(trip).data
            request_data = {
                "method": request.method,  # HTTP method (GET, POST, etc.)
                "url": request.build_absolute_uri(),  # Full URL of the request
                "headers": dict(request.headers),  # Convert headers to a dictionary
                "body": data,
            }
            send_request(request_data, response)
            return Response(response, status=status.HTTP_201_CREATED)

    def get(self, request, trip_id=None):
        if trip_id:
            trip = Trip.objects.get(id=trip_id)
            return Response(TripSerializer(trip).data)
        trips = Trip.objects.all()
        response = TripSerializer(trips, many=True).data
        request_data = {
            "method": request.method,  # HTTP method (GET, POST, etc.)
            "url": request.build_absolute_uri(),  # Full URL of the request
            "headers": dict(request.headers),  # Convert headers to a dictionary
            "body": request.body.decode("utf-8")
            if request.body
            else None,  # Request body (if exists)
        }
        try:
            send_request(request_data, response)
        except:
            return Response(response)
