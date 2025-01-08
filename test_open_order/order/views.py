import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem
from rest_framework import serializers
from opentelemetry import trace

from opentelemetry.trace import SpanKind
tracer = trace.get_tracer("django-app")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"


USER_SERVICE_URL = "http://127.0.0.1:8000/user/get"


class OrderListCreateView(APIView):
    def get_user_from_service(self, user_id):
        """
        Fetch user data from the external service using the user ID.
        """
        try:
            with tracer.start_as_current_span("get_user_from_service", kind=SpanKind.CLIENT) :
                # Assuming the user service returns a user with id and firstname
                response = requests.get(f"{USER_SERVICE_URL}/{user_id}")
                response.raise_for_status()
                user_data = response.json()
                return user_data
        except requests.exceptions.RequestException as e :
            return Response(f"error: {str(e)}",status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :
            return Response(f"error: {str(e)}",status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, *args, **kwargs):
        """
        Get the list of orders.
        """
        with tracer.start_as_current_span("order_get_span"):
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new order. User data is fetched from the external service.
        """
        with tracer.start_as_current_span("order_post_span") as span:

            user_id = request.data.get("user_id")
            user_data = self.get_user_from_service(user_id)
            span.set_attribute("user_id",user_id)
            for item in user_data:
                span.set_attribute(f"user_data : {item}",user_data[item])

            if not user_data:
                return Response(
                    {"error": "User data not found or service unavailable."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # If user data exists, create the order
            customer_name = user_data.get("first_name")
            data = {
                "user_id": user_id,
                "customer_name": customer_name,
                "total_price": request.data.get("total_price"),
            }
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemListCreateView(APIView):
    def get(self, request, *args, **kwargs):
        """
        Get the list of order items for a specific order.
        """
        with tracer.start_as_current_span("orderItem_get_span"):
            order_id = self.kwargs.get("order_id")
            order = Order.objects.get(id=order_id)
            items = order.items.all()
            serializer = OrderItemSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """
        Create a new order item for a specific order.
        """
        with tracer.start_as_current_span("orderItem_post_span"):

            order_id = self.kwargs.get("order_id")
            order = Order.objects.get(id=order_id)
            data = request.data
            data["order"] = order.id
            serializer = OrderItemSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
